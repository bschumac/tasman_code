


fls <- list.files("C:/PhD/Tasman_OP/smooth_converted/", pattern = "irg", full.names = T)




merged_df <- read.csv(fls[1], skip = 1)
merged_df <- merged_df[3:nrow(merged_df),]



for (i in seq(2,length(fls))){
  print(i)
  new_df <- read.csv(fls[i], skip = 1)
  new_df <- new_df[3:nrow(new_df),]
  merged_df <- rbind(merged_df,new_df)
  
  
} 

merged_df_rough <- merged_df

merged_df_rough$RECORD <- NULL 
merged_df_rough$diag_sonic<- NULL 
merged_df_rough$diag_irga <- NULL
merged_df_rough$cell_tmpr <- NULL
merged_df_rough$cell_press <- NULL
merged_df_rough$CO2_sig_strgth <- NULL
merged_df_rough$H2O_sig_strgth <- NULL

#merged_df_rough$Timestamp2 <- 
merged_df_rough$nmea_sentence.1. <- as.character(merged_df_rough$nmea_sentence.1.)
merged_df_rough$Ux <- as.character(merged_df_rough$Ux)
merged_df_rough$Uy <- as.character(merged_df_rough$Uy)
merged_df_rough$Uz <- as.character(merged_df_rough$Uz)
merged_df_rough$Ts <- as.character(merged_df_rough$Ts)
merged_df_rough$CO2 <- as.character(merged_df_rough$CO2)
merged_df_rough$H2O <- as.character(merged_df_rough$H2O)
merged_df_rough$TIMESTAMP <- as.character(merged_df_rough$TIMESTAMP)



time <- substr(merged_df_rough$nmea_sentence.1.,8,13)
date <- substr(merged_df_rough$nmea_sentence.1.,54,59)
merged_df_rough$TIMESTAMP_UTC <- paste(date,time)
excl = !grepl("E", date)
excl[1] = FALSE

merged_df_rough <- merged_df_rough[excl,]

#merged_df_rough

merged_df_rough[merged_df_rough == "NAN"] <- NA
merged_df_rough$Ux <- as.numeric(merged_df_rough$Ux)
merged_df_rough$Uy <- as.numeric(merged_df_rough$Uy)
merged_df_rough$Uz <- as.numeric(merged_df_rough$Uz)
merged_df_rough$Ts <- as.numeric(merged_df_rough$Ts)
merged_df_rough$CO2 <- as.numeric(merged_df_rough$CO2)
merged_df_rough$H2O <- as.numeric(merged_df_rough$H2O)

merged_df_rough <- merged_df_rough[complete.cases(merged_df_rough),]


merged_df_rough$TIMESTAMP_UTC <- strptime(merged_df_rough$TIMESTAMP_UTC, format = "%d%m%y %H%M%S", tz="GMT")

write.csv(merged_df_rough,"C:/PhD/Tasman_OP/rough_cleaned.csv")



merged_df_rough$TIMESTAMP_UTC_char <- as.character(merged_df_rough$TIMESTAMP_UTC)










plot(merged_df_rough$count)




merged_df_rough$count <- as.numeric(ave(merged_df_rough$TIMESTAMP_UTC, merged_df_rough$TIMESTAMP_UTC, FUN = length))

test <- table(merged_df$TIMESTAMP_UTC_char)
df_test<- as.data.frame(test)
library(plyr) 

plot(df_test$Freq)

test <- table(numbers)

test1 <- df_test[df_test$Freq<20,]
nrow(df_test)

