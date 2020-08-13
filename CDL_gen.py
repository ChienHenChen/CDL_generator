import math
import os

#printnode functions
def printnode(Voltagenode,start,end):
	header=0;
	for i in range(start,end):
		if i == start:
			fhand.write("+ ")
		elif i%8 == 0:
			fhand.write("+ ")
		fhand.write(Voltagenode+"<"+str(end-1-header)+"> ")
		if i == end-1:
			fhand.write("\n")
			break
		elif i%8 == 7:
			fhand.write("\n")
		header=header+1;

#printsignal functions
def printsignal(signal,i,bank):
	if bank ==1:
		fhand.write("+ "+signal+"\n")
	elif bank>=2:
		fhand.write("+ "+signal+"<"+str(i)+">\n")	

#Get the SRAM macro configurations info.#
while True:
	#Get the SRAM Capacity value#
	while True:
		while True:	
			try:
				Capacity=int(input("Please enter the SRAM macro capacity (bits) :"))
				Capacity_base2=math.log(Capacity,2)
				Capacity_base2_round=math.floor(Capacity_base2)
				break
			except:
				print("Please re-enter the correct SRAM macro capacity")
		if Capacity_base2 - Capacity_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct SRAM macro capacity")

	#Get the SRAM # of Bank value#
	while True:
		while True:	
			try:
				Bank=int(input("Please enter the number of Banks of this SRAM macro :"))
				Bank_base2=math.log(Capacity,2)
				Bank_base2_round=math.floor(Capacity_base2)
				break
			except:
				print("Please re-enter the correct SRAM macro capacity")
		if Bank_base2 - Bank_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the number of Banks of this SRAM macro")

	#Get the SRAM Wordsize value#
	while True:
		while True:	
			try:
				Wordsize=int(input("Please enter the wordsize of this SRAM macro (bits) :"))
				Wordsize_base2=math.log(Wordsize,2)
				Wordsize_base2_round=math.floor(Wordsize_base2)
				break
			except:
				print("Please re-enter the wordsize value of this SRAM macro")
		if Wordsize_base2 - Wordsize_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct wordsize value")

	#Get the SRAM # of Rows value#
	while True:
		while True:	
			try:
				Rows=int(input("Please enter the number of Rows in the local bank:"))
				Rows_base2=math.log(Rows,2)
				Rows_base2_round=math.floor(Rows_base2)
				break
			except:
				print("Please re-enter the number of Rows in in the local bank")
		if Rows_base2 - Rows_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct number of Rows value")

	#Get the SRAM # of Columns value#
	while True:
		while True:	
			try:
				Columns=int(input("Please enter the number of Columns in the local bank:"))
				Columns_base2=math.log(Columns,2)
				Columns_base2_round=math.floor(Columns_base2)
				break
			except:
				print("Please re-enter the number of Columns in the local bank")
		if Columns_base2 - Columns_base2_round == 0:
			break
		else:
			print("The number is not based on 2. Please re-enter the correct number of Columns value")
	
	NumberofWord=int(Capacity/Wordsize)	
	NumberofWordPerBank=int((Capacity/Bank)/Wordsize)	
	CMUX_C=int(Columns/Wordsize)
	CMUX_R=int(((Capacity/Bank)/Wordsize)/Rows)
	if CMUX_C == CMUX_R:
		CMUX=CMUX_C
		break
	else:
		print("The information of SRAM macro configuration is something wrong. Please double check and re-enter")

print("The configuration of this SRAM cdl file is as following")
print("Capacity:"+str(Capacity))
print("Bank:"+str(Bank))
print("Wordsize:"+str(Wordsize))
print("NumberofWord:"+str(NumberofWord))
print("NumberofWordPerBank:"+str(NumberofWordPerBank))
print("Rows:"+str(Rows))
print("Columns:"+str(Columns))
print("CMUX:"+str(CMUX))

#Address bit count calculation
TOTAL_ADDR_BIT_COUNT=int(math.log(NumberofWord,2))
LOCAL_ADDR_BIT_COUNT=int(math.log(NumberofWordPerBank,2))
BANK_ADDR_BIT_COUNT=TOTAL_ADDR_BIT_COUNT-LOCAL_ADDR_BIT_COUNT
COLUMN_BIT_COUNT=int(math.log(CMUX,2))
ROW_BIT_COUNT=LOCAL_ADDR_BIT_COUNT-COLUMN_BIT_COUNT

#information of INA and INB
if Rows > 8:
	sqrt_rows=math.sqrt(Rows)
	sqrt_rows_log2=math.log(sqrt_rows,2)
	IN_power=math.ceil(sqrt_rows_log2)
	IN_number=int(2**IN_power)
elif Rows <=8:
	IN_number=Rows

##Open a cdl file to write##
rundir=os.getcwd() # pwd function
output_dir=rundir+"/output/"
cdl_file_name="SRAM_"+str(NumberofWordPerBank)+"X"+str(Wordsize)+"XCM"+str(CMUX)+"XBANK"+str(Bank)+".cdl"
fhand=open(output_dir+cdl_file_name,"w")
fhand.write("***************"+"SRAM_"+str(NumberofWordPerBank)+"X"+str(Wordsize)+"XCM"+str(CMUX)+"XBANK"+str(Bank)+"***************\n")

control_unit_file_name="CU_"+str(NumberofWordPerBank)+"X"+str(Wordsize)+"XCM"+str(CMUX)+"XBANK"+str(Bank)+".cdl"

##Include the SRAM Auxcell as inputs##
rundir=os.getcwd() # pwd function
input_dir=rundir+"/input/"
fhand.write(".inc '"+input_dir+"WLDriver.cdl'\n")
fhand.write(".inc '"+input_dir+"PreCharge.cdl'\n")
fhand.write(".inc '"+input_dir+"ColMux.cdl'\n")
fhand.write(".inc '"+input_dir+"SenseAmp.cdl'\n")
fhand.write(".inc '"+input_dir+"WriteDriver.cdl'\n")
fhand.write(".inc '"+input_dir+"DIDO.cdl'\n")
fhand.write(".inc '"+input_dir+"Bitcell.cdl'\n")
fhand.write(".inc '"+input_dir+control_unit_file_name+"'\n")
fhand.write("********************************************"+"\n")

###Create the sub-circuits ColPeri_N (N=CMUX)###
fhand.write("\n")
ColPeri_subckt="ColPeri"+str(CMUX)
fhand.write(".SUBCKT " + ColPeri_subckt + "\n")

#BL/BLB
printnode("BL",0,CMUX)
printnode("BLB",0,CMUX)

#CK
fhand.write("+ CK\n")

#CSEL
printnode("CSEL",0,CMUX)

fhand.write("+ DIN DOUT PRCH SAE VDD VSS WEN\n")

##instantiate PreCharge and ColMux sub-circuits
for i in range(CMUX):
	fhand.write("XIPRCH<"+str(i)+"> "+"BL<"+str(i)+"> " +"BLB<"+str(i)+"> "+"PRCH VDD "+"PreCharge\n")

for i in range(CMUX):
	fhand.write("XICMUX<"+str(i)+"> "+"BL<"+str(i)+"> " +"BLB<"+str(i)+"> "+"CSEL<"+str(i)+"> "+"DL DLB VDD VSS "+ "ColMux\n")

##instantiate SenseAmp, WriteDriver and DIDO
fhand.write("XISA DL DLB PRCH SAE VDD VSS SenseAmp\n")
fhand.write("XIWD DIN_DFF VDD VSS DL DLB WEN WriteDriver\n")
fhand.write("XIDIDO CK DIN DIN_DFF DL DLB DOUT VDD VSS DIDO\n" )
fhand.write(".ENDS\n")

##top-level column peripherial circuits##
fhand.write("\n")
fhand.write(".SUBCKT ColumnPeriphery\n")

#BL
printnode("BL",0,Columns)

#BLB
printnode("BLB",0,Columns)

#CK
fhand.write("+ CK\n")

#CSEL
printnode("CSEL",0,CMUX)

#DIN
printnode("DIN",0,Wordsize)


#DOUT
printnode("DOUT",0,Wordsize)

#PRCH, SAE, VDD, VSS & WEN
fhand.write("+ PRCH SAE VDD VSS WEN\n")

##instantiate sub-circuits ColPeri_N (N=CMUX)###
for i in range(Wordsize):
	fhand.write("XI"+ColPeri_subckt+"<"+str(i)+">\n")
	printnode("BL",i*CMUX,(i+1)*CMUX)
	printnode("BLB",i*CMUX,(i+1)*CMUX)
	fhand.write("+ CK\n")
	printnode("CSEL",0,CMUX)
	fhand.write("+ DIN<"+str(i)+"> "+"DOUT<"+str(i)+"> "+"PRCH SAE VDD VSS WEN "+ColPeri_subckt+"\n")
fhand.write(".ENDS\n")

##top-level Row peripherial circuits##
fhand.write("\n")
fhand.write(".SUBCKT RowPeriphery\n")
#INA
printnode("INA",0,IN_number)
#INB
printnode("INB",0,IN_number)
#VDD VSS
fhand.write("+ VDD VSS\n")
#WL
printnode("WL",0,Rows)
## Rows >8, use pre-decoder scheme
if Rows > 8 and ROW_BIT_COUNT % 2 ==0:
	for i in range(0,IN_number):
		for j in range(0,IN_number):
			fhand.write("XIWLD<"+str(i*IN_number+j)+"> "+"INA<"+str(j)+"> "+"INB<"+str(i)+"> VDD VSS "+"WL<"+str(i*IN_number+j)+"> " +"WLDriver\n")
			if j == IN_number-1:
				i=i+1
elif Rows > 8 and ROW_BIT_COUNT % 2 ==1:
	IN_half=int(IN_number/2)
	IN_sq=IN_half**2
	for i in range(0,IN_half):
		for j in range(0,IN_half):
			fhand.write("XIWLD<"+str(i*IN_half+j)+"> "+"INA<"+str(j)+"> "+"INB<"+str(i)+"> VDD VSS "+"WL<"+str(i*IN_half+j)+"> " +"WLDriver\n")
			if j == IN_half-1:
				i=i+1
	for i in range(0,IN_half):
		for j in range(0,IN_half):
			fhand.write("XIWLD<"+str(i*IN_half+j+IN_sq)+"> "+"INA<"+str(j+IN_half)+"> "+"INB<"+str(i+IN_half)+"> VDD VSS "+"WL<"+str(i*IN_half+j+IN_sq)+"> " +"WLDriver\n")
			if j == IN_half-1:
				i=i+1
## Rows <= 8, don't use pre-decoder scheme
elif Rows<=8:
	for i in range(0,Rows):
		fhand.write("XIWLD<"+str(i)+"> "+"INA<"+str(i)+"> "+"INB<"+str(i)+"> VDD VSS "+"WL<"+str(i)+"> " +"WLDriver\n")
fhand.write(".ENDS\n")

##2x2 Bit-cell##
fhand.write("\n")
fhand.write(".SUBCKT Bitcell_2X2 BL<1> BL<0> BLB<1> BLB<0> VDD VSS WL<1> WL<0>\n")
fhand.write("XIUR BL<1> BLB<1> VDD VSS WL<1> Bitcell\n")
fhand.write("XIUL BL<0> BLB<0> VDD VSS WL<1> Bitcell\n")
fhand.write("XIDR BL<1> BLB<1> VDD VSS WL<0> Bitcell\n")
fhand.write("XIDL BL<0> BLB<0> VDD VSS WL<0> Bitcell\n")
fhand.write(".ENDS\n")

##Bitcell Rowsx2 sub-circuits##
fhand.write("\n")

#BL<1:0> BLB<1:0> VDD VDD
Bitcell_RowsX2="Bitcell_"+str(Rows)+"X2"
fhand.write(".SUBCKT " +Bitcell_RowsX2+" BL<1> BL<0> BLB<1> BLB<0> VDD VSS\n")

#WL<Rows:0>
printnode("WL",0,Rows)

#instantiate Bitcell_2x2
for i in range(int(Rows/2)):
	fhand.write("XIROW<"+str(i)+"> "+"BL<1> BL<0> BLB<1> BLB<0> VDD VSS "+"WL<"+str(i*2+1)+"> "+"WL<"+str(i*2)+"> Bitcell_2X2\n" )
fhand.write(".ENDS\n")

##SRAM Bitcell Array"
fhand.write("\n")
SRAM_Bitcell_Array="CellArray"+"Row"+str(Rows)+"XCol"+str(Columns)
fhand.write(".SUBCKT "+SRAM_Bitcell_Array+"\n")

#BL
printnode("BL",0,Columns)

#BLB
printnode("BLB",0,Columns)

#VDD VSS
fhand.write("+ VDD VSS\n")

#WL
printnode("WL",0,Rows)

##instantiate Bitcell Rowsx2
for i in range(int(Columns/2)):
	fhand.write("XICOL<"+str(i)+"> "+"BL<"+str(i*2+1)+"> "+"BL<"+str(i*2)+"> "+"BLB<"+str(i*2+1)+"> "+"BLB<"+str(i*2)+"> \n")
	fhand.write("+ VDD VSS\n")
	printnode("WL",0,Rows)
	fhand.write("+ "+Bitcell_RowsX2+"\n")
fhand.write(".ENDS\n")

##Single-bank level SRAM CDL netlist##
fhand.write("\n")
local_bank_name="SRAM_"+str(NumberofWordPerBank)+"X"+str(Wordsize)+"XCM"+str(CMUX)
fhand.write(".SUBCKT "+local_bank_name+"\n")

#CK
fhand.write("+ CK\n")

#CSEL
printnode("CSEL",0,CMUX)

#DIN
printnode("DIN",0,Wordsize)

#DOUT
printnode("DOUT",0,Wordsize)

#INA & INB
printnode("INA",0,IN_number)
printnode("INB",0,IN_number)

#PRCH
fhand.write("+ PRCH\n")

#SAE VDD VSS WEN
fhand.write("+ SAE VDD VSS WEN\n")

##Instantiate bitcell array
fhand.write("XICELL\n")

#BL
printnode("BL",0,Columns)

#BLB
printnode("BLB",0,Columns)

#VDD VSS
fhand.write("+ VDD VSS\n")

#WL
printnode("WL",0,Rows)

fhand.write("+ "+SRAM_Bitcell_Array+"\n")

##Instantiate Row periphery
fhand.write("XIRowPeri\n")

#INA & INB
printnode("INA",0,IN_number)
printnode("INB",0,IN_number)

#VDD VSS
fhand.write("+ VDD VSS\n")

#WL
printnode("WL",0,Rows)
fhand.write("+ RowPeriphery\n")

##Instantiate Column periphery
fhand.write("XIColPeri\n")

#BL
printnode("BL",0,Columns)

#BLB
printnode("BLB",0,Columns)

#CK
fhand.write("+ CK\n")

#CSEL
printnode("CSEL",0,CMUX)

#DIN
printnode("DIN",0,Wordsize)

#DOUT
printnode("DOUT",0,Wordsize)

#PRCH, SAE, VDD, VSS & WEN
fhand.write("+ PRCH SAE VDD VSS WEN ColumnPeriphery\n")
fhand.write(".ENDS\n")

##top level SRAM CDL netlist##
fhand.write("\n")
toplevel_name="SRAM_"+str(NumberofWordPerBank)+"X"+str(Wordsize)+"XCM"+str(CMUX)+"XBANK"+str(Bank)
fhand.write(".SUBCKT "+toplevel_name+"\n")
#ADDR
printnode("ADDR",0,TOTAL_ADDR_BIT_COUNT)

#CE CLK
fhand.write("+ CE CLK\n")

#DIN
printnode("DIN",0,Wordsize)

#DOUT
printnode("DOUT",0,Wordsize)

#VDD VSS & WE
fhand.write("+ VDD VSS WE\n")

##Instantiate local bank

for i in range(Bank):
	fhand.write("XIBANK<"+str(i)+">\n")
	#CK
	printsignal("CK",i,Bank)
	#CSEL
	if Bank<=1:
		printnode("CSEL",0,CMUX)
	elif Bank>=2:
		CSEL_BANK="CSEL"+str(i)	
		printnode(CSEL_BANK,0,CMUX)
	#DIN
	printnode("DIN",0,Wordsize)
	#DOUT
	if Bank<=1:
		printnode("DOUT",0,Wordsize)
	elif Bank>=2:
		DOUT_BANK="DOUT"+str(i)	
		printnode(DOUT_BANK,0,Wordsize)
	
	#INA & INB
	if Bank<=1:
		printnode("INA",0,IN_number)
		printnode("INB",0,IN_number)
	elif Bank>=2:
		INA_BANK="INA"+str(i)
		INB_BANK="INB"+str(i)
		printnode(INA_BANK,0,IN_number)
		printnode(INB_BANK,0,IN_number)
	#PRCH
	printsignal("PRCH",i,Bank)	
	#SAE
	printsignal("SAE",i,Bank)
	#VDD & VSS
	fhand.write("+ VDD VSS\n")
	#WEN
	printsignal("WEN",i,Bank)
	#locak bank name
	fhand.write("+ "+local_bank_name+" \n")

	
##instantiate 1CU for single/multi-bank SRAM
if Bank==1:
	fhand.write("XICU\n")
	printnode("ADDR",0,TOTAL_ADDR_BIT_COUNT)
	fhand.write("+ CE CK CLK\n")
	printnode("CSEL",0,CMUX)
	printnode("INA",0,IN_number)
	printnode("INB",0,IN_number)
	fhand.write("+ PRCH\n")
	fhand.write("+ SAE VDD VSS WE WEN\n")
	fhand.write("+ "+"CU_"+str(NumberofWordPerBank)+"X"+str(Wordsize)+"XCM"+str(CMUX)+"XBANK"+str(Bank)+"\n")

elif Bank>=2:
	fhand.write("XICU\n")
	printnode("ADDR",0,TOTAL_ADDR_BIT_COUNT)
	fhand.write("+ CE\n")
	printnode("CK",0,Bank)
	fhand.write("+ CLK\n")
	for i in range(Bank):
		CSEL_string="CSEL"+str(i)
		printnode(CSEL_string,0,CMUX)
	for i in range(Bank):
		DOUT_string="DOUT"+str(i)
		printnode(DOUT_string,0,Wordsize)
	printnode("DOUT",0,Wordsize)
	for i in range(Bank):
		INA_string="INA"+str(i)
		printnode(INA_string,0,IN_number)
	for i in range(Bank):
		INB_string="INB"+str(i)
		printnode(INB_string,0,IN_number)
	printnode("PRCH",0,Bank)
	printnode("SAE",0,Bank)
	fhand.write("+ VDD VSS\n")
	fhand.write("+ WE\n")
	printnode("WEN",0,Bank)
	fhand.write("+ "+"CU_"+str(NumberofWordPerBank)+"X"+str(Wordsize)+"XCM"+str(CMUX)+"XBANK"+str(Bank)+"\n")

fhand.write(".ENDS\n")
fhand.close()


