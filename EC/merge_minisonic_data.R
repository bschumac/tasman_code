
# Relative Path variables - find the data used in /shared_Tasman_03_2020/Ben/EC/Tier00/
# These are the to TOA5 converted files from the TasmanOp 2020


# Rough or smooth
prefix <- "Rough"
data_path <- "C:/PhD/Tasman_OP/"

fls <- list.files(paste0(data_path,prefix,"_converted/"), pattern = "minisonic", full.names = T)

# sort filelst 
library(gtools)
fls <- mixedsort(fls)
# read first file
merged_df <- read.csv(fls[1], skip = 1)
merged_df <- merged_df[3:nrow(merged_df),]


# read all other files
for (i in seq(2,length(fls))){
  print(i)
  new_df <- read.csv(fls[i], skip = 1)
  new_df <- new_df[3:nrow(new_df),]
  merged_df <- rbind(merged_df,new_df)
  
  
} 


# read second set of files to merge the timestamps to retrieve the GPS string 
fls2 <- list.files(paste0("C:/PhD/Tasman_OP/",prefix,"_converted/"), pattern = "irg", full.names = T)

# sort filelst 
library(gtools)
fls2 <- mixedsort(fls2)
# read first file
merged_df_irg <- read.csv(fls2[1], skip = 1)
merged_df_irg <- merged_df_irg[3:nrow(merged_df_irg),]


# read all other files
for (i in seq(2,length(fls2))){
  print(i)
  new_df_irg <- read.csv(fls2[i], skip = 1)
  new_df_irg <- new_df_irg[3:nrow(new_df_irg),]
  merged_df_irg <- rbind(merged_df_irg,new_df_irg)
  
  
} 
# create time df to merge the timestamps and the GPS string to the minisonic data
time_df <- data.frame(merged_df_irg$TIMESTAMP,merged_df_irg$RECORD, merged_df_irg$nmea_sentence.1. )
colnames(time_df) <- c("TIMESTAMP", "RECORD", "nmea_sentence.1.")

# Merge time_df with the minisonic df
merged_df_minisonic <- merge(merged_df,time_df, by="TIMESTAMP")

# delete all columns which are not needed
merged_df_minisonic$RECORD.x <- NULL
merged_df_minisonic$RECORD.y <- NULL

merged_df_minisonic$nmea_sentence.1. <- as.character(merged_df$nmea_sentence.1.)
merged_df_minisonic$TIMESTAMP <- as.character(merged_df_minisonic$TIMESTAMP)
merged_df_minisonic$WIND_X <- as.character(merged_df_minisonic$WIND_X)
merged_df_minisonic$WIND_Y <- as.character(merged_df_minisonic$WIND_Y)
merged_df_minisonic$WIND_Z <- as.character(merged_df_minisonic$WIND_Z)
merged_df_minisonic$WIND_pitch <- as.character(merged_df_minisonic$WIND_pitch)
merged_df_minisonic$WIND_roll <- as.character(merged_df_minisonic$WIND_roll)
merged_df_minisonic$WIND_direction <- as.character(merged_df_minisonic$WIND_direction)

# exclude all stamps without a GPS string
time <- substr(merged_df_minisonic$nmea_sentence.1.,8,13)
date <- substr(merged_df_minisonic$nmea_sentence.1.,54,59)
merged_df_minisonic$TIMESTAMP_UTC <- paste(date,time)
excl = !grepl("E", date)
excl[1] = FALSE

merged_df_minisonic <- merged_df_minisonic[excl,]


# convert to numeric 
merged_df_minisonic[merged_df_minisonic == "NAN"] <- NA
merged_df_minisonic$WIND_X <- as.numeric(merged_df_minisonic$WIND_X)
merged_df_minisonic$WIND_Y <- as.numeric(merged_df_minisonic$WIND_Y)
merged_df_minisonic$WIND_Z <- as.numeric(merged_df_minisonic$WIND_Z)
merged_df_minisonic$WIND_pitch <- as.numeric(merged_df_minisonic$WIND_pitch)
merged_df_minisonic$WIND_roll <- as.numeric(merged_df_minisonic$WIND_roll)
merged_df_minisonic$WIND_direction <- as.numeric(merged_df_minisonic$WIND_direction)

# write csv in a clean version and a version with GPS string
write.csv(merged_df_minisonic,paste0("C:/PhD/Tasman_OP/",prefix,"_minisonic_merged.csv"))

merged_df$nmea_sentence.1. <- NULL
merged_df$nmea_sentence.2. <- NULL
merged_df$TIMESTAMP <- NULL

write.csv(merged_df_minisonic,paste0("C:/PhD/Tasman_OP/",prefix,"_minisonic_merged_clean.csv"))

