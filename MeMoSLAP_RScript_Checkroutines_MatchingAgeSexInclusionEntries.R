###########################################################################
#
# Author: Sven Passmann
# created: 23.08.2024
# changed: 
#
# checks PANAS/TES, demographics and last questionnaire excel files
# whether the entries for age, sex, and inclusion etc. matches
#
#
###########################################################################


# libaries/packages
library(readxl)
library(dplyr)
library(tidyverse)

rm(list = ls())
graphics.off()

# setting working directory
setwd("Y:/01_Studien/00_FOR5429_MeMoSLAP/RU_Experiments_Participants/11_PreliminaryAnalysis/Data")

###########################################################################

# read in data
Neuro <- read_excel ("MeMoSLAP_Data_Neuropsych_Questionnaires.xlsx")
Panas <- read_excel ("MeMoSLAP_Data_PANAS_TES.xlsx", sheet = "PANAS")
AE <- read_excel ("MeMoSLAP_Data_PANAS_TES.xlsx", sheet = "TES")
LastQuest <- read_excel ("MeMoSLAP_Data_Last_Questionnaire.xlsx")


# reducing dataframes
Neuro <- Neuro [, c(1:6)]
Panas <- Panas [, c(1:6)]
AE <- AE [, c(1:6)]
LastQuest <- LastQuest [, c(1:6)]


# rename columns
zusatz <- "_Neuro"
# Schleife über die Spaltennamen des Dataframes
for (i in seq_along(names(Neuro))) {
  names(Neuro)[i] <- paste(names(Neuro)[i], zusatz, sep = "")
}

zusatz <- "_Panas"
for (i in seq_along(names(Panas))) {
  names(Panas)[i] <- paste(names(Panas)[i], zusatz, sep = "")
}

zusatz <- "_AE"
for (i in seq_along(names(AE))) {
  names(AE)[i] <- paste(names(AE)[i], zusatz, sep = "")
}

zusatz <- "_Last"
for (i in seq_along(names(LastQuest))) {
  names(LastQuest)[i] <- paste(names(LastQuest)[i], zusatz, sep = "")
}


# combine dataframes
Combined <- cbind (Neuro, Panas, AE, LastQuest)



###########################################################################
# checking subject-wise

# for subjects
Combined_subj <- Combined [, c(1,7,13,19)]
Combined_subj <- Combined_subj %>%
  rowwise() %>%
  mutate(AllEqual = all(c_across(everything()) == first(c_across(everything()))))


# for projects
Combined_proj <- Combined [, c(1,2,8,14,20)]
Combined_proj <- Combined_proj %>%
  rowwise() %>%
  mutate(AllEqual = all(c_across(2:5) == first(c_across(2:5))))


# for groups
Combined_group <- Combined [, c(1,3,9,15,21)]
Combined_group <- Combined_group %>%
  rowwise() %>%
  mutate(AllEqual = all(c_across(2:5) == first(c_across(2:5))))


# for switched
Combined_switch <- Combined [, c(1,4,10,16,22)]
Combined_switch <- Combined_switch %>%
  rowwise() %>%
  mutate(AllEqual = all(c_across(2:5) == first(c_across(2:5))))


# for in & exclude
Combined_inex <- Combined [, c(1,5,11,17,23)]
Combined_inex <- Combined_inex %>%
  rowwise() %>%
  mutate(AllEqual = all(c_across(2:5) == first(c_across(2:5))))


# for sex
Combined_sex <- Combined [, c(1,6,12,18,24)]
Combined_sex <- Combined_sex %>%
  rowwise() %>%
  mutate(AllEqual = all(c_across(2:5) == first(c_across(2:5))))



# combine dataframes
Combined_check <- cbind (Combined_subj, Combined_proj, Combined_group, Combined_switch,
                         Combined_inex, Combined_sex)

# save
write.table(Combined_check, file = "Y:/01_Studien/00_FOR5429_MeMoSLAP/RU_IT/Server/02_Checking_Routines/Output/MeMoSLAP_Report_EqualData_Demographic_P137.tsv", 
            sep = "\t", row.names = FALSE, col.names = TRUE, quote = FALSE)

