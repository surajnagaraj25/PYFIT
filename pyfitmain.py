#PYFIT
#author: Suraj Nagaraja
#RUID: 189005203

#main
from datetime import date
from pyfitlib import Person, Report, Dietreport, Workoutreport, bodyfat
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier


col_names = ['height(cm)','waist(cm)','shoulder(cm)','body-type','5','6','7','8','9','10','11']
data = pd.read_csv('Bodymeasurements2.csv',names=col_names) #reading dataset from the CSV file
#print(data.shape)
#print(data.head(5))

dataset = data[['height(cm)','waist(cm)','shoulder(cm)','body-type']] #gettig rid of the extra columns with NaN values
#print(dataset.head(5))


array = dataset.values
X = array[:,0:3]       #array containing height,waist and shoulder data
Y = array[:,3]         #array containing the body-type data for the corresponding height,waist and shoulder values
validation_size = 0.20
seed = 7
X_train,X_validation,Y_train,Y_validation = model_selection.train_test_split(X,Y,test_size=validation_size,random_state=seed)

#using the knn classification algorithm
model = KNeighborsClassifier()
model.fit(X,Y)

#taking user inputs
name = input("What's your name?: ")
age = int(input("How old are you?: "))
weight = float(input("Enter your weight(pounds): "))
height = float(input("Enter your height(cm): "))
waist = float(input("Enter your waist circumference(cm): "))
shoulder = float(input("Enter your shoulder circumference(cm): "))
p1 = Person(name,age,weight,height,waist,shoulder) #an object of Person class created for the user

bfat = bodyfat(p1.getWeight(),p1.getWaist()) # bfat function calculates the body fat percentage

today = str(date.today()) #saving current date in a variable to use for record keeping
list1 = [p1.getName(),p1.getWeight(),p1.getWaist(),bfat,today]
#saving users data in a file for record keeping and progress tracking
userfile = open("userdata.txt","a")
for item in list1:
    userfile.write("%s\t"%item)
userfile.write("\n")
userfile.close()

#predicting body-type based on values input by the user
Xnew = [[p1.getHeight(),p1.getWaist(),p1.getShoulder()]]
Ynew = model.predict(Xnew)

print("\n"+p1.getName()+", you belong to the '"+Ynew[0]+"' category.") #printing the user's body-type

prompt = input("\nReport or progress tracking? (r/p): ") #asking user whether he wishes to download the report or track progress

while prompt not in ['r','p']: #program accepts only 'r' and 'p' as inputs to avoid unnecessary input errors
    prompt = input("You have provided an invalid input. Please enter 'r' for report and 'p' for progress tracking: ")
   
if prompt == 'r': #printing the reports if user inputs 'r'
    r1 = Dietreport(Ynew[0]) #creating an object of Dietreport class
    r2 = Workoutreport(Ynew[0]) #creating an object of Workoutreport class
    print("\n"+Ynew[0]+" diet and workout tips have been downloaded by your system.")
    r1.Summary()
    r2.Summary()
    det = input("Would you like to download detailed workout and diet plans? You will be charged $10:(y/n) ") #asking user if he wants detailed reports
    while det not in ['y','n']:
        det = input("\nYou have provided an invalid input. Please enter 'y' for detailed plans and 'n' to dismiss: ")
    
    if det == 'y': #printing detailed reports if user inputs 'y'
        r1.Detailed()
        r2.Detailed()
        print("\nYou have opted for the complete package! You have been charged $10.\
 \nThanks for using PYFIT. Get ready for a newer, fitter you!")
    elif det =='n':
        print("\nThank you for using PYFIT. All the best!")

elif prompt == 'p': #progress tracking part
    col_name = ['Weight','Waist','Bodyfat','Date','extra']
    data = pd.read_csv("userdata.txt",sep='\t',names=col_name)
    data = data.drop(['extra'],axis = 1)
    #print(data)
    usrdata1 = data.loc[p1.getName()] #locating the paticular users data based on name
    usrdata = usrdata1.drop_duplicates(subset='Date',keep='first') #ignoring duplicate entries for a particular user which were made on the same date
    print(usrdata) #displaying the users records
    #plotting
    fig, ax1 = plt.subplots()
    ax1.plot(usrdata['Date'],usrdata['Weight'],'b')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Weight (Pounds)')
    ax2 = ax1.twinx()
    ax2.plot(usrdata['Date'],usrdata['Bodyfat'],'g')
    ax2.set_ylabel('Body Fat Percentage')
    ax1.legend(loc = 2)
    ax2.legend(loc = 1)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()













