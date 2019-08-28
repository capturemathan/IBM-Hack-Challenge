import Tkinter as tk
from Tkinter import filedialog as fd
import sys
import os
import csv
import re
import os.path,subprocess
from subprocess import STDOUT,PIPE

parsed=[]
parsedindex=[]
class Browse(tk.Frame):
    def __init__(self, master, initialdir='', filetypes=()):
        super().__init__(master)
        self.filepath = tk.StringVar()
        self.trace1path = tk.StringVar()
        self.trace2path = tk.StringVar()
        self.method_path = tk.StringVar()
        self.methods = ''
        self.count=0
        self.depth_value=0

        self._initaldir = initialdir
        self._filetypes = filetypes

        self.x=''
        self.trace1=tk.StringVar()
        self.trace2=tk.StringVar()

        self.texts=tk.StringVar()
        self.converted_texts=tk.StringVar()

        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self._entry = tk.Entry(self, textvariable=self.filepath)
        self._entry2 = tk.Entry(self, textvariable=self.trace1path)
        self._entry3 = tk.Entry(self, textvariable=self.trace2path)
        self.method_entry = tk.Entry(self, textvariable=self.method_path)

        self.depth_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)

        self._xtrace = tk.Button(self, text='Generate Xtrace/Method Trace',command=self.xtrace)
        self.m_trace = tk.Button(self, text='Generate Application trace', command=self.mtrace)
        self._convert = tk.Button(self, text='Convert',command=self.convert)
        self.method_names = tk.Label(self, text="Enter the methods")
        self.stack_depth = tk.Label(self,text='Set your StackTrace')

        self._browse = tk.Button(self, text="Browse...", command=self.browse)
        self._browse2 = tk.Button(self, text="Browse...", command=self.browse2)
        self._browse3 = tk.Button(self, text="Browse...", command=self.browse3)

        self._parse = tk.Button(self, text='Parse',command=self.parse)
        self._compare = tk.Button(self, text='Compare',command=self.compare)


        self.T = tk.Text(root, height=2, width=60)
        self.T.pack(side=tk.LEFT,fill=tk.Y)
        self.S=tk.Scrollbar(root)
        self.S.pack(side=tk.RIGHT, fill=tk.Y)

    def _display_widgets(self):
        self._entry.pack(fill='x', expand=True)
        self._browse.pack(anchor='se',pady=5)
        self.method_names.pack(anchor='center',pady=10)
        self.method_entry.pack(expand=tk.YES, fill=tk.X)
        self.stack_depth.pack(anchor='center',pady=10)
        self.depth_slider.pack()
        self._xtrace.pack(anchor='center',padx=50,pady=10)
        self.m_trace.pack(anchor='center',padx=50)
        self._convert.pack(anchor='center',padx=50,pady=10)
        self._parse.pack(anchor='center',padx=50,pady=10)

        self._entry2.pack(fill='x', expand=True)
        self._browse2.pack(anchor='se',pady=5)
        self._entry3.pack(fill='x', expand=True)
        self._browse3.pack(anchor='se',pady=10)
        self._compare.pack(anchor='center',padx=50,pady=10)
        

    def browse(self):
        self.x=fd.askopenfilename(initialdir=self._initaldir,
                                             filetypes=self._filetypes)
        
        self.filepath.set(self.x)

        print(self.filepath)


    def browse2(self):
        self.trace1=fd.askopenfilename(initialdir=self._initaldir,
                                             filetypes=self._filetypes)
        
        self.trace1path.set(self.trace1)

        print(self.trace1)

    def browse3(self):
        self.trace2=fd.askopenfilename(initialdir=self._initaldir,
                                             filetypes=self._filetypes)
        
        self.trace2path.set(self.trace2)

        print(self.trace2)


    def xtrace(self):

        print("Xtrace generating.....")
        self.count=self.count+1
        self.methods=self.method_entry.get()
        self.depth_value=self.depth_slider.get()
        os.system('java -classpath '+self.x+' -Xtrace:methods='+str(self.methods)+',stackdepth='+str(self.depth_value)+',maximal=mt,output=traceout'+str(self.count)+'.trc')

        print("Xtrace generated")

    def mtrace(self):
    	import_statement= 'import com.ibm.jvm.Trace;'
    	templates_dec='static int handle;static String[] templates;'
    	class_name='"Main"'
    	function_name='""'
    	entry_trace='Trace.trace( handle, 0,'+function_name+');'
    	exit_trace='Trace.trace( handle, 1, '+function_name +');'
    	indexfound=0;
    	javafile=self.x
    	w=javafile.split('/')
    	y=w[len(w)-1]
    	javaclass='"'+y.split('.')[0]+'"'
    	main_initialize='templates = new String[ 5 ];\n templates[ 0 ] = Trace.ENTRY+ "Entering %s";\ntemplates[ 1 ] = Trace.EXIT+ "Exiting %s";\n templates[ 2 ] = Trace.EVENT+ "Event id %d, text = %s";\ntemplates[ 3 ] = Trace.EXCEPTION + "Exception: %s";\n templates[ 4 ] = Trace.EXCEPTION_EXIT + "Exception exit from %s";\nhandle = Trace.registerApplication('+ javaclass+', templates );\nfor (int i = 0; i < args.length; i++ ) \n{ \nSystem.err.println( "Trace setting: " + args[ i ] );\nTrace.set( args[ i ] ); \n}\n Trace.trace( handle, 2, 1, "Trace initialized" );'
    	with open (javafile, "r") as myfile:
		    data=myfile.readlines()
		    index=[]
		    methods=[]
		    parsedindex=[]
		    packages=[]
		    package_index=-1
		    classes=[]
		    classes_index=[]
		    public_class=""
		    for i,line in enumerate(data):
		        if "public" in line:
		            methods.append(line)
		            index.append(i)
		        if "class" in line:
		        	if line not in methods:
		        		methods.append(line)
		        		index.append(i)     
		        elif "private" in line:
		            methods.append(line)
		            index.append(i)
		        elif "static" in line:
		            methods.append(line)
		            index.append(i)
		        elif "package" in line:
		        	packages.append(line)
		        	package_index=i
		    for p,i in enumerate(methods):
		        if "new" in i:
		            pass
		        elif "class" in i:
		        	for k in range(index[p]-1,len(data)):
		        		if "{" in data[k]:
		        			classes_index.append(k)
		        			break
		        else:
		            parsed.append(i)
		            parsedindex.append(index[p])
		    output=data

		    

		    output[package_index+1]+=import_statement
		    for x in classes_index:	
		    	output[x]+=templates_dec			
		    for i,line in enumerate(parsed):
		    	if "main" in line:
		    		indexfound=i
		    		output[parsedindex[indexfound]+1]+=main_initialize
		    		main_initialize=""
		    		break
		    
		    for x in parsedindex:
		    	flag=0
		    	for j in range(x,len(output)):
		    		if "{" in output[j] and flag==0:
		    			function_name=output[x]
		    			output[j]+=(entry_trace)
		    			flag=1

		    f=open(javafile,"w")
		    for i in output:
		    	f.write(i)
		    f.close()

		    print('Application trace Generating.....')
		    os.system('javac '+javafile)
		    sys.stdout=open("output.txt","w")
		    os.system('java '+javaclass+' iprint='+javaclass+' > out.txt')
     
    def convert(self):
    	print('converting')
    	os.system('java com.ibm.jvm.format.TraceFormat traceout'+str(self.count)+'.trc')

    	with open('traceout'+str(self.count)+'.trc.fmt','rb') as f:
    		self.converted_texts=f.read()
        

    	self.T.insert(tk.CURRENT,self.converted_texts)
        
    def compare(self):
        print("comparing")
        check='0'
        with open(self.trace1,'rb') as csv_file1:
            with open(self.trace2,'rb') as csv_file2:
                with open('report'+str(self.count)+'.txt','wb') as writefile:
                    csv_as_list1 = [row1 for row1 in csv_file1 if row1 is not "\0"]
                    csv_as_list2 = [row2 for row2 in csv_file2 if row2 is not "\0"]
                    for row1 in csv_as_list1:
                        try:
                            for row2 in csv_as_list2:
                                try:
                                    if(row1!=row2):
                                        writefile.write(row1)
                                        check='1'
                                        break
                                except:
                                    pass
                        except:
                            pass
                    if(check=='0'):
                        writefile.write('No change'.decode())
               
       

    def parse(self):
        print("parsing")
        # mylines=[]
        array=[]
        array2=[]
        array3=[]
        array4=[]
        word=""
        i=1
        with open ('traceout'+str(self.count)+'.trc.fmt', 'rb') as myfile:
            with open ('sample'+str(self.count)+'.txt', 'wb') as final:
                for myline in myfile:
                    i=i+1
                    if(i>67):
                        final.write(myline)

        final_lines=[]
        each_line=[]
        with open('sample'+str(self.count)+'.txt','rb') as formatted:
            for final_lines in formatted:
                each_line.append(re.split('\*| ',final_lines.decode()))

            for p in range(len(each_line)):
                for i in each_line[p]:
                    j = list(i)
                    array.append(j)

                for k in array:
                    if len(k)!=0:
                        array2.append(k)
                
                for m in array2:
                    for n in m:
                        word+=n
                    array3.append(word)
                    word=""

                array4.append(array3)
                array=[]
                array2=[]
                array3=[]

            with open('xtrace'+str(self.count)+'.csv', 'w+') as csvfile:
                filewriter = csv.writer(csvfile,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['Thread Id','Entry timestamp','Exit Timestamp','Event Timestamp','Exception Timestamp','TraceEntry'])
                for i in array4:
                    if(i[3]=='Entry'):
                        filewriter.writerow([i[2],i[0],'','','',i[4]])
                    elif(i[3]=='Exit'):
                        filewriter.writerow([i[2],'',i[0],'','',i[4]])
                    elif(i[3]=='Event'):
                        filewriter.writerow([i[2],'','',i[0],'',i[4]])
                    elif(i[3]=='Exception'):
                        filewriter.writerow([i[2],'','',i[0],'',i[4]])
                print('over')
                      


if __name__ == '__main__':
    root=tk.Tk()
    file_browser = Browse(root, initialdir=r"C:\Users")
    file_browser.pack(fill='x', expand=True)
    root.mainloop()
