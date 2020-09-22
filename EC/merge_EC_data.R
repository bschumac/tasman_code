


fls <- list.files("/mnt/Seagate_Drive1/Tasman_OP/Rough_converted/", pattern = "irg", full.names = T)




merged_df <- read.csv(fls[1], skip = 1)
merged_df <- merged_df[3:nrow(merged_df),]



for (i in seq(2,length(fls))){
  print(i)
  new_df <- read.csv(fls[i], skip = 1)
  new_df <- new_df[3:nrow(new_df),]
  merged_df <- rbind(merged_df,new_df)
  
  
} 

merged_df$RECORD <- NULL 
merged_df$diag_sonic<- NULL 
merged_df$diag_irga <- NULL
merged_df$cell_tmpr <- NULL
merged_df$cell_press <- NULL
merged_df$CO2_sig_strgth <- NULL
merged_df$H2O_sig_strgth <- NULL

#merged_df$Timestamp2 <- 
merged_df$nmea_sentence.1. <- as.character(merged_df$nmea_sentence.1.)

time <- substr(merged_df$nmea_sentence.1.,8,13)
date <- substr(merged_df$nmea_sentence.1.,54,59)

#merged_df$time <- substr(merged_df$nmea_sentence.1.,8,13)

merged_df$TIMESTAMP_UTC <- strptime(paste(date,time), format = "%d%m%y %H%M%S", tz="GMT")

merged_df$TIMESTAMP_UTC_char <- as.character(merged_df$TIMESTAMP_UTC)
merged_df <- merged_df[complete.cases(merged_df$TIMESTAMP_UTC),]


merged_df$count <- as.numeric(ave(merged_df$TIMESTAMP_UTC, merged_df$TIMESTAMP_UTC, FUN = length))

test <- table(merged_df$TIMESTAMP_UTC_char)
df_test<- as.data.frame(test)
library(plyr) 

plot(df_test$Freq)

test <- table(numbers)

test1 <- df_test[df_test$Freq<20,]
nrow(df_test)

