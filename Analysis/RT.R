# RT Data Analysis 
library(tidyverse)
library(ggpubr)
library(rstatix)
library(dplyr)
# Load data
setwd('/Users/YJC/Dropbox/ExpRecord_HSI')
dial_dat <- read.table('RT_D_Merge.txt',
                  header = FALSE)
dial_dat[,8] <- rep('Dial', 226)
colnames(dial_dat) <- c('ID', 'nStimulus', 'Resp', 'Stimuli',
                   'T/F', 'RT','Timestamp' , 'Device')

joy_dat <- read.table('RT_J_Merge.txt',
                       header = FALSE)
joy_dat[,8] <- rep('Joystick', 203)
colnames(joy_dat) <- c('ID', 'nStimulus', 'Resp', 'Stimuli',
                        'T/F', 'RT','Timestamp', 'Device' )


dat <- rbind(dial_dat, joy_dat)

set.seed(1234)
dplyr::sample_n(dat, 10)
str(dat) # long data already

dat %>%
    group_by(Stimuli, Device) %>%
    get_summary_stats(RT, type = "mean_sd")

# Plot

bxp <- ggboxplot(
    dat, x = "Stimuli", y = "RT",
    color = "Device", palette = "jco")
bxp


# Statistics