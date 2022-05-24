library(Quandl)
source('utilities.R')

library(tidyr)
library(dplyr)
library(Quandl)
library(RcppRoll)
library(ggplot2)
library(purrr)
library(lubridate)
library(xts)
library(ggplot2)
library(scales)
library(plotly)
library(PerformanceAnalytics)

Quandl.api_key(Sys.getenv('QUANDL_API_KEY'))

ewma_vectorized_v2 <- function(x, a) {
  s1 <- x[1]
  sk <- s1
  s <- vapply(x[-1], function(x) sk <<- (1 - a) * x + a * sk, 0)
  s <- c(s1, s)
  return(s)
}

analyzeRollingReturn <- function(ticker,lag=5,lambda=2)
{
  dt <- lubridate::today()
  start <- dt %m+% months(-12)
  
  price_dly <- Quandl.datatable('SHARADAR/SEP',ticker=ticker,paginate = T)
  price_dly <- price_dly %>% filter(date>=start) %>% select(date,close) %>% arrange(date)
  names(price_dly) <- c('Date','Price')
  price_dly$Price <- as.numeric(price_dly$Price)
  price_xts <- price_dly$Price %>% xts(order.by=price_dly$Date)
  
  rtn_dly <- Return.calculate(price_xts)[2:nrow(price_xts),]
  
  rolling_rtn <- rollapply(rtn_dly,lag,function(x) prod(1+x)-1)
  
  names(rolling_rtn) <- 'RollingReturn'
  rolling_rtn <- as.data.frame(rolling_rtn[lag:nrow(rolling_rtn),])
  rolling_rtn$Date <- rownames(rolling_rtn) %>% as.Date
  rownames(rolling_rtn) <- NULL
  
  sd <- sd(rolling_rtn$RollingReturn)
  
  last_dt <- rolling_rtn$Date[nrow(rolling_rtn)]
  last <- rolling_rtn[rolling_rtn$Date==last_dt,'RollingReturn']
  # Get the percent of the latest rolling return
  tmp <- sort(rolling_rtn$RollingReturn)
  pct <- which(tmp==last)/length(tmp)
  
  summary <- data.frame(Ticker=ticker,Date=last_dt,Last=last,Pct=pct,Mean=mean(rolling_rtn$RollingReturn),Sd=sd)
  
  U2Sd <- summary$Mean+lambda*summary$Sd
  D2Sd <- summary$Mean-lambda*summary$Sd
  
  summary$U2Sd <- U2Sd
  summary$D2Sd <- D2Sd
  
  rolling_rtn$U2Sd <- U2Sd
  rolling_rtn$D2Sd <- D2Sd
  
  rolling_rtn <- rolling_rtn %>% left_join(price_dly,by='Date')
  
  coef <- (max(rolling_rtn$Price)-min(rolling_rtn$Price))/(max(rolling_rtn$RollingReturn)-min(rolling_rtn$RollingReturn))
  #coef <- median(rolling_rtn$Price)/median(rolling_rtn$RollingReturn)/10
  
  print(ggplot(rolling_rtn)+geom_col(aes(x=Date,y=RollingReturn))+geom_line(aes(x=Date,y=U2Sd),color='blue',linetype='dashed')+geom_line(aes(x=Date,y=D2Sd),color='red',linetype='dashed')+ggtitle(paste(ticker,lag,'day rolling return till',dt))+theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +geom_line(aes(x=Date,y=Price/coef,group=1),color='orange')+ scale_y_continuous(
    
    # Features of the first axis
    name = "Rolling Return",
    
    # Add a second axis and specify its features
    sec.axis = sec_axis(~.*coef, name="Price")
  )+scale_x_date(breaks = pretty_breaks(10)))
  
  return(summary)
}

analyzeEWMAReturn <- function(ticker,alpha=0.1)
{
  dt <- lubridate::today()
  start <- dt %m+% months(-12)
  
  price_dly <- Quandl.datatable('SHARADAR/SEP',ticker=ticker,paginate = T)
  price_dly <- price_dly %>% filter(date>=start) %>% select(date,close) %>% arrange(date)
  names(price_dly) <- c('Date','Price')
  price_dly$Price <- as.numeric(price_dly$Price)
  price_xts <- price_dly$Price %>% xts(order.by=price_dly$Date)
  
  rtn_dly <- Return.calculate(price_xts)[2:nrow(price_xts),]
  
  rolling_rtn <- rtn_dly %>% as.numeric
  rolling_rtn <- data.frame(Date=index(rtn_dly),RollingReturn=ewma_vectorized_v2(rolling_rtn,alpha))
  
  sd <- sd(rolling_rtn$RollingReturn)
  last <- rolling_rtn$Date[nrow(rolling_rtn)]
  summary <- data.frame(Ticker=ticker,Date=last,Last=rolling_rtn[rolling_rtn$Date==last,'RollingReturn'],Mean=mean(rolling_rtn$RollingReturn),Sd=sd)
  
  U2Sd <- summary$Mean+2*summary$Sd
  D2Sd <- summary$Mean-2*summary$Sd
  
  summary$U2Sd <- U2Sd
  summary$D2Sd <- D2Sd
  
  rolling_rtn$U2Sd <- U2Sd
  rolling_rtn$D2Sd <- D2Sd
  
  rolling_rtn <- rolling_rtn %>% left_join(price_dly,by='Date')
  
  coef <- (max(rolling_rtn$Price)-min(rolling_rtn$Price))/(max(rolling_rtn$RollingReturn)-min(rolling_rtn$RollingReturn))
  
  print(ggplot(rolling_rtn)+geom_col(aes(x=Date,y=RollingReturn))+geom_line(aes(x=Date,y=U2Sd),color='blue',linetype='dashed')+geom_line(aes(x=Date,y=D2Sd),color='red',linetype='dashed')+ggtitle(paste(ticker,alpha,'alpha EWMA return till',dt))+theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +geom_line(aes(x=Date,y=Price/coef,group=1),color='orange')+ scale_y_continuous(
    
    # Features of the first axis
    name = "EWMA Return",
    
    # Add a second axis and specify its features
    sec.axis = sec_axis(~.*coef, name="Price")
  )+scale_x_date(breaks = pretty_breaks(10)))
  
  return(summary)
}

analyzeDrawdown <- function(ticker,lambda=2)
{
  dt <- lubridate::today()
  start <- dt %m+% months(-12)
  
  price_dly <- Quandl.datatable('SHARADAR/SEP',ticker=ticker,paginate = T)
  price_dly <- price_dly %>% filter(date>=start) %>% select(date,close) %>% arrange(date)
  names(price_dly) <- c('Date','Price')
  price_dly$Price <- as.numeric(price_dly$Price)
  price_xts <- price_dly$Price %>% xts(order.by=price_dly$Date)
  
  rtn_dly <- Return.calculate(price_xts)[2:nrow(price_xts),]
  
  drawdown <- Drawdowns(rtn_dly) %>% as.data.frame
  #rolling_rtn <- rollapply(rtn_dly,lag,function(x) prod(1+x)-1)
  
  names(drawdown) <- 'Drawdown'
  drawdown$Date <- rownames(drawdown) %>% as.Date
  rownames(drawdown) <- NULL
  
  sd <- sd(drawdown$Drawdown)
  
  last_dt <- drawdown$Date[nrow(drawdown)]
  last <- drawdown[drawdown$Date==last_dt,'Drawdown']
  # Get the percent of the latest rolling return
  tmp <- sort(drawdown$Drawdown)
  pct <- which(tmp==last)/length(tmp)
  
  summary <- data.frame(Ticker=ticker,Date=last_dt,Last=last,Pct=pct,Mean=mean(drawdown$Drawdown),Sd=sd)
  
  U2Sd <- summary$Mean+lambda*summary$Sd
  D2Sd <- summary$Mean-lambda*summary$Sd
  
  summary$U2Sd <- U2Sd
  summary$D2Sd <- D2Sd
  
  drawdown$U2Sd <- U2Sd
  drawdown$D2Sd <- D2Sd
  
  drawdown <- drawdown %>% left_join(price_dly,by='Date')
  
  coef <- (max(drawdown$Price)-min(drawdown$Price))/(max(drawdown$Drawdown)-min(drawdown$Drawdown))
  
  print(ggplot(drawdown)+geom_line(aes(x=Date,y=Drawdown))+geom_line(aes(x=Date,y=D2Sd),color='red',linetype='dashed')+ggtitle(paste(ticker,'day drawdown till',dt))+theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +geom_line(aes(x=Date,y=Price/coef,group=1),color='orange')+ scale_y_continuous(
    
    # Features of the first axis
    name = "Drawdown",
    
    # Add a second axis and specify its features
    sec.axis = sec_axis(~.*coef, name="Price")
  )+scale_x_date(breaks = pretty_breaks(10)))
  
  return(summary)
}

lag=5
lambda = 2
analyzeRollingReturn('AAPL',lag,lambda) 
analyzeRollingReturn('TSLA',lag) 
analyzeRollingReturn('AMD',lag)  
analyzeRollingReturn('PYPL',lag) 
analyzeRollingReturn('BILI',lag)

alpha=0.5
analyzeEWMAReturn('AAPL',alpha) 
analyzeEWMAReturn('TSLA',alpha) 
analyzeEWMAReturn('AMD',alpha)  
analyzeEWMAReturn('PYPL',alpha) 
analyzeEWMAReturn('BABA',alpha)

analyzeDrawdown('TSLA')
analyzeDrawdown('AMD')
analyzeDrawdown('BABA')
