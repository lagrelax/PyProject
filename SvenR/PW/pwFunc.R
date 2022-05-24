setwd('D:/Research/R/SvenProject/')

library(Quandl)
source('utilities.R')

library(tidyr)
library(dplyr)
library(RcppRoll)
library(ggplot2)
library(purrr)

Quandl.api_key(Sys.getenv('QUANDL_API_KEY'))


getCurrentPEPercentile <- function(ticker,value='eps')
{
  ticker <- toupper(ticker)
  price <- Quandl.datatable('SHARADAR/SEP',ticker=ticker,paginate = T)
  fundamental <- Quandl.datatable('SHARADAR/SF1',ticker=ticker,dimension='ARQ')
  
  if(value == 'eps')
    rolling_eps <- fundamental[,c('datekey','epsusd')] %>% mutate(eps=epsusd)
  
  if(value=='ebitda')
    rolling_eps <- fundamental[,c('datekey','ebitda','shareswa')] %>% 
    mutate(eps=ebitda/shareswa)
  
  if(value=='revenue')
    rolling_eps <- fundamental[,c('datekey','revenue','shareswa')] %>% 
    mutate(eps=revenue/shareswa)
  
  # Calculate the TTM growth-rate as well
  rolling_eps <- rolling_eps %>% arrange(datekey)
  n=nrow(rolling_eps)
  tmp <- data.frame(datekey=rolling_eps$datekey[5:n],TTM=rolling_eps$eps[1:(n-4)])
  rolling_eps <- rolling_eps %>% left_join(tmp) %>% mutate(growth=(eps-TTM)/TTM)
  
  rolling_eps <- rolling_eps %>% dplyr::arrange(datekey) %>% 
    mutate(eps4=roll_sum(eps,4,align='right',fill=NA))
  
  tmp=rolling_eps$datekey
  
  idx <- price$date %>% sapply(function(x) max(which(tmp<=x)))
  
  daily_pe <- price %>% select(date,closeadj) %>% mutate(close=closeadj,closeadj=NULL)
  daily_pe$datekey <- tmp[idx]
  
  daily_pe <- daily_pe %>% filter(!is.na(datekey)) %>% left_join(rolling_eps,by='datekey')
  daily_pe <- daily_pe %>% mutate(close=as.numeric(close),pe=close/eps4) %>% na.omit
  daily_pe <- daily_pe %>% mutate(peg=pe/growth)
  daily_pe <- daily_pe %>% arrange(desc(date))
  
  # Other data: pb
  daily_pb <- fundamental %>% select(datekey, pb)
  daily_pe <- daily_pe %>% left_join(daily_pb,by='datekey')
  if(nrow(daily_pe)==0) return(NULL)
  
  current_pe <- daily_pe[1,]
  
  # To adress the issue the negative value polluting the percentile
  minpe <- min(daily_pe$pe)
  minpeg <- min(daily_pe$peg)
  pe_percentile <- ecdf(abs(daily_pe$pe))
  peg_percentile <- ecdf(abs(daily_pe$peg))
  
  # 0-low, 1-high
  result <- c(pe_percentile(abs(current_pe$pe)),peg_percentile(abs(current_pe$peg)))
  names(result) <- c('PE','PEG')
  
  if(value=='ebitda')
    daily_pe <- daily_pe %>% mutate(pebitda=pe) %>% select(-pe)
  if(value=='revenue')
    daily_pe <- daily_pe %>% mutate(ps=pe) %>% select(-pe)
  
  return(list(hist=daily_pe,current_percntile=result))
}

pwFunc <- function(ticker,prev_date)
{
  tmp <- getCurrentPEPercentile(ticker)
  hist <- tmp$hist
  prev <- as.Date(prev_date)
  p0 <- hist %>% filter(date==prev) %>% select(close) %>% pull
  p <- hist[1,'close']
  
  rtns = xts(hist[1:253,'close'],order.by = hist$date[1:253])
  rtns = Return.calculate(rtns)[-1,] 
  
  print(head(hist,5))
  print(c('Change'=(p-p0)/p0))
  print(c('1Y Sd'=sd(rtns[,1])))
  print(tmp$current_percntile)

  return(tmp)  
}

result <- pwFunc('fb',as.Date('2022-04-29'))
