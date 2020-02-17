#### R commands for plotting and implementation of the statistics, trees and
###random forests presented in the related publication Ehret, Katharina, and
###Maite Taboada (submitted) "The interplay of complexity and subjectivity in
###opinionated discourse". Submitted to Discourse Studies.

#### set the stage
# load libraries
library(dplyr)
library(Hmisc)
library(caTools)
library(ggplot2)
library(ggparty)
library(reshape2)
library(partykit)
library(caret)
library(ggcorrplot)

# load data: aggregate_totals_normalised.csv
df = read.csv("aggregate_totals_normalised.csv")

# get statistical overview
stats = describe(df)

observations = length(df$textType)

# check for correlations between predictors
corVars = data.frame(df$year, df$morphComplexity, df$synComplexity, df$overallComplexity, df$subjectiveNegative, df$subjectivePositive, df$modals, df$connectives, df$adverbials)

# create nice column names
names(corVars) = c("year", "morphological complexity", "syntactic complexity", "overall complexity", "subjective negative", "subjective positive", "modals", "connectives", "adverbials")

# calculate correlations and plot them
cors = cor(corVars)

ggcorrplot(cors, hc.order = TRUE, type = "lower", outline.col = "white",
ggtheme = ggplot2::theme_gray, colors = c("midnightblue", "white", "lightblue"))


#### conditional inference trees
# set seed for reproducibility
set.seed(234)

# split data into test and training set
split = sample.split(df$textType, SplitRatio = 0.7)
train = subset(df, split==TRUE)
test = subset(df, split==FALSE)

# tree formula with fine-grained distinctions; 9 predictors
formula = textType ~ year + morphComplexity + synComplexity +
overallComplexity + subjectiveNegative + subjectivePositive + modals +
connectives + adverbials

# tune tree parameters and build model
tunegrid <- expand.grid(
  mincriterion = c(0.9,0.95,0.99), #critical value of the test statistic
  minbucket = c(600,800,1000), #minimum sum of weights in a terminal node
  maxsurrogate = c(0,3,6) #number of surrogate splits
)

# create list of tuned trees
tree.list <- list()

for (i in 1:nrow(tunegrid)){
  mycontrols = ctree_control(mincriterion = tunegrid[i,1], 
                                 minbucket = tunegrid[i,2], 
				 maxsurrogate = tunegrid[1,3])
  tree.list[[i]] = ctree(formula, data = train, control = mycontrols)
}  

# assess model performance
for (i in 1:nrow(tunegrid)) {

  print("========================================================")

  print(paste("parameters",

              tunegrid[i,1],tunegrid[i,2],tunegrid[i,3]))

  myct = tree.list[[i]]
  confMat = table(predict(myct), train$textType)
  train.acc = sum(diag(confMat))/sum(confMat)
  test.acc = mean(predict(myct, newdata=test)==test$textType)

  print(confMat)

  print(paste("training accuracy:",train.acc))
  print(paste("test accuracy:",test.acc))

  tunegrid$train.acc[i] <- train.acc
  tunegrid$test.acc[i] <- test.acc 
}

# check which settings return the highest prediction accuracy in training and test dataset

View(tunegrid)

which.max(tunegrid$train.acc)
which.max(tunegrid$test.acc)

# select tree
mytree = tree.list[[1]]

## plot the tree 
# create nice egde labels
treedat = ggparty(mytree)$data

breaks = unlist(treedat$breaks_label)

cleanbreaks = lapply(breaks, function(x) gsub("NA > *NA\\*|NA <= NA\\*", "", x))

roundbreaks = lapply(cleanbreaks, function(x) round(as.numeric(x), digits = 2))

signs = lapply(breaks, function(x) gsub("[0-9]*[.-][0-9]*", "", x))

# plot basic tree
p = ggparty(mytree) +
  geom_edge() +
  geom_edge_label(mapping = aes(label=paste(signs,roundbreaks))) +
  geom_node_label(line_list= list(aes(label=splitvar), aes(label=paste("node", id))), line_gpar= list(list(size=10, parse=T), list(size=8)), ids="inner") +
  geom_node_label(line_list = list(aes(label=paste("node", id)), aes(label=paste("n =", nodesize))), line_gpar= list(list(size=10), list(size=10)), ids="terminal", nudge_y = 0.013, nudge_x = 0.01)

# plot bars
p + geom_node_plot(gglist = list(geom_bar(aes(x =textType, fill=textType)),
scale_fill_manual(values=c("midnightblue", "lightblue",
"firebrick"), guide=F), theme(axis.title=element_blank(),
axis.text.x=element_text(angle=45, hjust=1), axis.ticks.x =
element_blank())), nudge_y= -0.015)

# print
pdf("ctree.pdf", width=20, height=10)


## run tuning process across multiple data splits to test for robustness
# create 20 splits
R <- 20
trng.list <- list(R)
test.list <- list(R)
for (r in 1:R){
  trng.index <- sample.int(n = nrow(df),
                             size = nrow(df)*0.7,
                             replace = FALSE)
  trng.list[[r]] = df[trng.index,]
  test.list[[r]] = df[-trng.index,]
} 

# create lists to store all models
trng.acc <- matrix(ncol = nrow(tunegrid), nrow = R)
test.acc <- matrix(ncol = nrow(tunegrid), nrow = R)

for (r in 1:R){
  train=trng.list[[r]]
  test=test.list[[r]]

  for (i in 1:nrow(tunegrid)){
  mycontrols = ctree_control(mincriterion = tunegrid[i,1], 
                                 minbucket = tunegrid[i,2], 
                                 maxsurrogate = tunegrid[i,3])
				
  myct = ctree(formula, data = train, control = mycontrols)
  
  trng.acc[r,i] = mean(predict(myct) ==train$textType)
  test.acc[r,i] = mean(predict(myct, newdata=test)==test$textType)
  }
  
}

colnames(trng.acc) <- colnames(test.acc) <- 
                    paste(tunegrid$mincriterion,
                            tunegrid$minbucket,
                            tunegrid$maxsurrogate,sep="_")

# create boxplots of training/test errors for 20 splits
par(mar=c(6,5,4,4))

boxplot(trng.acc, main="Boxplot: Training Error of 20 Splits",
        las=2) 

boxplot(test.acc, main="Boxplot: Test Error of 20 Splits",
        las=2)


#### grow conditional random forests

# set seed for reproducible results
set.seed(234)

# split data for testing prediction accuracy
fsplit = sample.split(df$textType, SplitRatio = 0.7)

ftrain = subset(df, fsplit==TRUE)
ftest = subset(df, fsplit==FALSE)

# forest formula
myform = textType ~ year + morphComplexity + synComplexity +
overallComplexity + subjectiveNegative + subjectivePositive + modals +
connectives + adverbials

# model discussed in the related publication
model = cforest(myform, data = ftrain, control = ctree_control(), ntree=500)

# additional models with more trees
model1000 = cforest(myform, data = ftrain, control = ctree_control(), ntree=1000)

model2000 = cforest(myform, data = ftrain, control = ctree_control(), ntree=2000)


# calculate prediction accuracy of the model
# confusion matrix
cm = table(predict(model), ftrain$textType)

# accuracy
acc = sum(diag(cm))/sum(cm)

# use model to classify test data
testPred = predict(model, newdata=ftest, type="response")

# calculate prediction accuracy of model for test data
# confusion matrix
tcm = table(testPred, as.factor(ftest$textType))

#accuracy
tacc = sum(diag(tcm))/sum(tcm)

#calculate conditional variable importance
myvarimp = varimp(model1000, conditional = T)

#plot variable importance
myvarimp = read.csv("varimp500.csv")

#nice predictor labels
niceLabels = c("Year", "Morphological complexity", "Syntactic complexity", "Overall complexity", "Subjective negative", "Subjective positive", "Modals", "Connectives", "Adverbials")

myvarimp$predictor = niceLabels

#plot
p = ggplot(myvarimp, aes(reorder(myvarimp$predictor, myvarimp$importance),importance)) +
geom_col(aes(fill=importance)) +
scale_fill_gradient2(mid = "lightblue", high="midnightblue") +
coord_flip() +
labs(x=" ", y="Variable importance", col="Importance") +
theme(axis.ticks.y=element_blank())


ggsave()




