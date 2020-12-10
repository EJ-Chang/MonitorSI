# OSD Data Analysis 
library(tidyverse)
library(ggpubr)
library(rstatix)
# Load data
setwd('/Users/YJC/Dropbox/ExpRecord_HSI/D_1')
dat <- read.table('OSD_D_Merge.txt',
                  header = FALSE)
colnames(dat) <- c('ID', 'reqRow', 'reqCol', 'Resp', 
                   'iRow', 'iCol', 'T/F', 'stepToGoal',
                   'RT','Timestamp' )

library(dplyr)

set.seed(1234)
dplyr::sample_n(dat, 10)
str(dat)

# Clear data

# Plot

# Statistics