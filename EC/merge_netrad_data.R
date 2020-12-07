
prefix <- "smooth"


fls <- list.files(paste0("C:/PhD/Tasman_OP/",prefix,"_converted/"), pattern = "Net_Rad", full.names = T)

library(gtools)
fls <- mixedsort(fls)

merged_df <- read.csv(fls[1], skip = 1)
merged_df <- merged_df[3:nrow(merged_df),]



for (i in seq(2,length(fls))){
  print(i)
  new_df <- read.csv(fls[i], skip = 1)
  new_df <- new_df[3:nrow(new_df),]
  merged_df <- rbind(merged_df,new_df)
  
  
} 
head(merged_df)
merged_df$RECORD <- NULL
merged_df$BattV_Min <- NULL
merged_df$nmea_sentence.1. <- as.character(merged_df$nmea_sentence.1.)
merged_df$TIMESTAMP <- as.character(merged_df$TIMESTAMP)
merged_df$PanelT <- as.character(merged_df$PanelT)
merged_df$Incoming_SW_Avg <- as.character(merged_df$Incoming_SW_Avg)
merged_df$Outgoing_SW_Avg <- as.character(merged_df$Outgoing_SW_Avg)
merged_df$Incoming_LW_Avg <- as.character(merged_df$Incoming_LW_Avg)
merged_df$Outgoing_LW_Avg <- as.character(merged_df$Outgoing_LW_Avg)


time <- substr(merged_df$nmea_sentence.1.,8,13)
date <- substr(merged_df$nmea_sentence.1.,54,59)
merged_df$TIMESTAMP_UTC <- paste(date,time)
excl = !grepl("E", date)
excl[1] = FALSE

merged_df <- merged_df[excl,]


merged_df[merged_df == "NAN"] <- NA
merged_df$PanelT <- as.numeric(merged_df$PanelT)
merged_df$Incoming_SW_Avg <- as.numeric(merged_df$Incoming_SW_Avg)
merged_df$Outgoing_SW_Avg <- as.numeric(merged_df$Outgoing_SW_Avg)
merged_df$Incoming_LW_Avg <- as.numeric(merged_df$Incoming_LW_Avg)
merged_df$Outgoing_LW_Avg <- as.numeric(merged_df$Outgoing_LW_Avg)


write.csv(merged_df,paste0("C:/PhD/Tasman_OP/",prefix,"_rad_merged.csv"))

merged_df$nmea_sentence.1. <- NULL
merged_df$nmea_sentence.2. <- NULL
merged_df$TIMESTAMP <- NULL

write.csv(merged_df,paste0("C:/PhD/Tasman_OP/",prefix,"_rad_merged_clean.csv"))



