import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *
import sys
import os
import csv
import re
import os.path
import subprocess
from subprocess import STDOUT,PIPE
from tkinter import messagebox



## A frame for displaying check-buttons 
#
#  This class is used to create a frame which contains the checklist of the methods fetched from the program. The value of the checkboxes is also being noted using the state() method
class Checkbar(Frame):
    ## The constructor
    def __init__(self, parent=None, picks=[], side=LEFT):
        Frame.__init__(self, parent)
        self.vars = []
        ## @var vars
        #  This variable is used to pick the fetched methods which are checked so that the method trace is generated only for those methods. This variable is appended each time a fetched method is checked by the user
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=TOP, anchor='center', expand=NO)
            self.vars.append(var)

    ## Method to return the state of the checkbox
    #  @param self Instance of the class
    #  @return 0 if not selected
    #  @return 1 if selected
    def state(self):
        return map((lambda var: var.get()), self.vars)

## To create a layout and to position the widgets
#
#  This class creates a frame with the necessary widgets. The user needs to interact with this GUI in order to generate the trace files and compare them
class Browse(tk.Frame):
    ## The constructor.
    def __init__(self, master, initialdir='', filetypes=()):
        super().__init__(master)
        self.filepath = tk.StringVar()
        ## @var filepath
        #  Button to browse and select the path of java file
        self.trace1path = tk.StringVar()
        ## @var trace1path
        #  Button to browse and select the path of first trace file
        self.trace2path = tk.StringVar()
        ## @var trace2path
        #  Button to browse and select the path of second trace file
        self.method_path = tk.StringVar()
        ## @var method_path
        #  The methods whose trace needs to be created can be entered in this box
        self.methods = ''
        ## @var methods
        #  This variable takes the methods whose trace needs to be created as input
        self.count=0
        ## @var count
        #  This variable is used to keep track of the number of trace files generated to uniquely distinguish them
        self.depth_value=0
        ## @var depth_value
        #  This variable is used to set the depth of the trace file to be generated
        self.parsed=[]
        ## @var parsed
        #  This variable contains the lisr of all parsed methods
        self.parsedindex=[] 
        ## @var parsedindex
        #  This will hold the indices of the parsed methods in the input java file
        self._initaldir = initialdir
        ## @var _initaldir
        #  This variable is used to set the initial directory from which the files need to be taken
        self._filetypes = filetypes
        ## @var _filetypes
        #  This variable is used to set the type of file that is present in the directory
        
        self.x=''
        ## @var x
        #  Variable used to browse and select the path of java file
        self.trace1=tk.StringVar()
        ## @var trace1
        #  Variable used to browse and select the path of the first trace file
        self.trace2=tk.StringVar()
        ## @var trace2
        #  Variable used to browse and select the path of the second trace file
        self.tempvar=tk.BooleanVar()
        ## @var tempvar
        #  Temporary variable
        
        self.texts=tk.StringVar()
        ## @var texts
        #  Button to browse and select the path of java file
        self.converted_texts=tk.StringVar()
        ## @var converted_texts
        #  Button to browse and select the path of java file
        self.listmethodentry1=[]
        self.listmethodexit1=[]
        self.listmethodentry2=[]
        self.listmethodexit2=[]

        self._create_widgets()
        self._display_widgets()

    ## Method to create all the widgets
    #  @param self Instance of the class        
    def _create_widgets(self):
        self.javaSourceFile = tk.Entry(self, textvariable=self.filepath)
        ## @var javaSourceFile
        #  Button used to browse and select the path of java file
        self.traceCsv1 = tk.Entry(self, textvariable=self.trace1path)
        ## @var traceCsv1
        #  Button used to browse and select the path of the first trace file
        self.traceCsv2 = tk.Entry(self, textvariable=self.trace2path)
        ## @var traceCsv2
        #  Button used to browse and select the path of the second trace file
        self.method_entry = tk.Entry(self, textvariable=self.method_path)
        ## @var method_entry
        #  Text box used to enter the methods whose trace needs to be generated
        
        self.depth_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
        ## @var depth_slider
        #  Slider to adjust the depth of trace file generation
        
        self._xtrace = tk.Button(self, text='Generate Xtrace/Method Trace',command=self.xtrace)
        ## @var _xtrace
        #  Button to generate the xtrace of the given file
        self.m_trace = tk.Button(self, text='Generate Application trace', command=self.mtrace)
        ## @var m_trace
        #  Button to generate the application trace
        self.fetch_methods = tk.Button(self, text='Fetch Methods', command=self.fetch_methods)
        ## @var fetch_methods
        #  Button to fetch the methods from the java program
        self.checkbox=tk.Checkbutton(self)
        ## @var checkbox
        #  This variable is used to create the checkbuttons for the fetched methods, so that the users can choose their required methods
        self.convertXtraceToReadable = tk.Button(self, text='Convert',command=self.convert)
        ## @var convertXtraceToReadable
        #  Button to convert the trace file in hex format to human-readable format
        self.method_names = tk.Label(self, text="Enter the methods (*,w,methods of inbuilt java packages)")
        ## @var method_names
        #  This variable is used to get the method names from the user
        self.stack_depth = tk.Label(self,text='Set your StackTrace')
        ## @var stack_depth
        #  This variable is used to get the depth of the trace file to be generated
        
        self.javaFileBrowse = tk.Button(self, text="Browse...", command=self.browse)
        ## @var javaFileBrowse
        #  Variable used to browse and select the path of the java file
        self.traceCsv1Browse = tk.Button(self, text="Browse...", command=self.browse2)
        ## @var traceCsv1Browse
        #  Variable used to browse and select the path of the first trace file
        self.traceCsv2Browse = tk.Button(self, text="Browse...", command=self.browse3)
        ## @var traceCsv2Browse
        #  Variable used to browse and select the path of the second trace file
        
        self._compare = tk.Button(self, text='Compare',command=self.compare)
        ## @var _compare
        #  Button to compare the two selected trace files
        

        self.TraceSummary = tk.Text(root, height=2, width=60)
        ## @var TraceSummary
        #  This variable is used for creating a text box used to show the intermediate output
        self.TraceSummary.pack(side=tk.LEFT,fill=tk.Y)
        self.Scrollbar=tk.Scrollbar(root)
        ## @var Scrollbar
        #  This variable is used for creating a scrollbar in the gui
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    ## Method to display all the widgets
    #  @param self Instance of the class
    def _display_widgets(self):
        self.javaSourceFile.pack(fill='x', expand=True)
        self.javaFileBrowse.pack(anchor='se',pady=5)
        self.method_names.pack(anchor='center',pady=10)
        self.method_entry.pack(expand=tk.YES, fill=tk.X)
        self.stack_depth.pack(anchor='center',pady=10)
        self.depth_slider.pack()
        self._xtrace.pack(anchor='center',padx=50,pady=10)
        self.convertXtraceToReadable.pack(anchor='center',padx=50,pady=10)

        self.traceCsv1.pack(fill='x', expand=True)
        self.traceCsv1Browse.pack(anchor='se',pady=5)
        self.traceCsv2.pack(fill='x', expand=True)
        self.traceCsv2Browse.pack(anchor='se',pady=10)
        self._compare.pack(anchor='center',padx=50,pady=10)

        self.fetch_methods.pack(anchor='center',padx=50,pady=10)
        self.m_trace.pack(anchor='center',padx=50)

    ## This method is used to browse and select the java file whose trace needs to be created. This is given as a browse widget.
    #  @param self Instance of the class
    def browse(self):
        self.x=fd.askopenfilename(initialdir=self._initaldir,filetypes=self._filetypes)        
        self.filepath.set(self.x)
        print(self.filepath)


    ## This method is used to browse and select the first trace file which was generated and converted to human-readable form.
    #  @param self Instance of the class
    def browse2(self):
        self.trace1=fd.askopenfilename(initialdir=self._initaldir,filetypes=self._filetypes)
        self.trace1path.set(self.trace1)
        print(self.trace1)

    ## This method is used to browse and select the second trace file which was generated and converted to human-readable form.
    #  @param self Instance of the class
    def browse3(self):
        self.trace2=fd.askopenfilename(initialdir=self._initaldir,filetypes=self._filetypes)
        self.trace2path.set(self.trace2)
        print(self.trace2)


    ## This method is used to generate the Xtrace of the selected java file using the xtrace command. This generated trace file is in hex fomat and it needs to converted to human-readable format in order to compare them.
    #  @param self Instance of the class
    def xtrace(self):
        print("Xtrace generating.....")
        self.count=self.count+1
        self.methods=self.method_entry.get()
        self.depth_value=self.depth_slider.get()
        os.system('java -classpath '+self.x+' -Xtrace:methods='+str(self.methods)+',stackdepth='+str(self.depth_value)+',maximal=mt,output=traceout'+str(self.count)+'.trc')
        print("Xtrace generated")
        messagebox.showinfo(title=None, message='Xtrace is generated in trc format')



    ## Displays all the methods of the class. The methods are shown in the form of a checklist. The users can select the methods as per their requirements.
    #  @param self Instance of the class
    def fetch_methods(self):
        variable = tk.StringVar(self)
        variable.set("one")
        javafile=self.x
        with open (javafile, "r") as myfile:
            data=myfile.readlines()
            index=[]
            methods=[]
            self.parsedindex=[]
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
                    self.parsed.append(i)
                    self.parsedindex.append(index[p])
         
            self.checkbar=Checkbar(self,self.parsed)
            ## @var checkbar
            #  Button to browse and select the path of java file
            self.checkbar.pack(side=TOP,fill=X)
            messagebox.showinfo(title=None, message='Methods are fetched and displayed as checkbuttons')   



    ## A checklist was created when fetch_methods() was used. This method is used to create method trace for the methods which was selected from the checklist
    #  @param self Instance of the class
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
        self.checkbar_state=list(self.checkbar.state())
        ## @var checkbar_state
        #  This variable is used to check the state of the checkbox. This is used to pick the methods which are required to be traced.
        with open (javafile, "r") as myfile:
            data=myfile.readlines()
            index=[]
            methods=[]
            self.parsedindex=[]
            packages=[]
            package_index=-1
            classes=[]
            openbracketindex=[]
            stack=[]
            closebracketindex=[]
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
                elif "protected" in line:
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
                    self.parsed.append(i)
                    self.parsedindex.append(index[p])

            for i in self.parsedindex:
                for j in range(i,len(data)):
                    if "{" in data[j]:
                        openbracketindex.append(j)

    #openbracketindex=set(openbracketindex)

            for i in self.parsedindex:
                for j in range (i,len(data)):
                    if "{" in data[j]:
                        stack.append(j)
                    if "}" in data[j]:
                        stack.pop()
                        if len(stack)==0:
                            closebracketindex.append(j)
                            break
            output=data
            output[package_index+1]+=import_statement

            for x in classes_index: 
                output[x]+=templates_dec    

            for i,line in enumerate(self.parsed):
                if "main" in line:
                    indexfound=i
                    output[self.parsedindex[indexfound]+1]+=main_initialize
                    main_initialize=""
                    break
            
            for i,x in enumerate(self.parsedindex):
                if(self.checkbar_state[i]==1):
                    flag=0
                    for j in range(x,len(output)):
                        if "{" in output[j] and flag==0:
                            function_name='"'+output[x].strip()+'"'
                            entry_trace='Trace.trace( handle, 0,'+function_name+');'
                            output[j]+=(entry_trace)
                            flag=1

            for x in closebracketindex:
                output[x]=exit_trace+'}'

            f=open(javafile,"w")
            for i in output:
                f.write(i)
            f.close()

            print('Application trace Generating.....')
            os.system('javac '+javafile)
            cmd='java '+javaclass+' iprint='+javaclass
            with open('outs.txt','w') as out:
                return_code=subprocess.call(cmd,stdout=out)
            messagebox.showinfo(title=None, message='Application trace Generated')
     
    ## Initially the trace file was generated using xtrace() method. It converts the trace file in hex format to human-readable format
    #  @param self Instance of the class
    def convert(self):
        print('converting')
        os.system('java com.ibm.jvm.format.TraceFormat traceout'+str(self.count)+'.trc')

        with open('traceout'+str(self.count)+'.trc.fmt','rb') as f:
            self.converted_texts=f.read()
        
        messagebox.showinfo(title=None, message='Converted to Human Readable format')
        self.TraceSummary.insert(tk.CURRENT,self.converted_texts)
        
    ## Compares the two selected trace files which have been converted to csv format using the convert() method
    #  @param self Instance of the class
    def compare(self):
        print("comparing")
        check='0'
        with open(self.trace1,'r') as trace_file1:
            with open(self.trace2,'r') as trace_file2:
                with open('report'+str(self.count)+'.csv','w') as csvfile:
                    data=trace_file1.readlines()
                    instack=[]
                    outstack=[]
                    c=0
                    for i,line in enumerate(data):
                        if "Entry" in line:
                            if ">get" in line:
                                entry=line.split("Entry")
                                methodentry=entry[-1]
                                argument=methodentry.split(">")
                                argumententry=argument[-1]
                                instack.append(argumententry)
                        if "Exit" in line:
                            if "<get" in line:
                                exit=line.split("Exit")
                                methodexit=exit[-1]
                                outstack.append("Exit")
                                if(len(instack)!=0):
                                    self.listmethodentry1.append(instack.pop())
                                    self.listmethodexit1.append(outstack[-1])

                    data=trace_file2.readlines()
                    instack=[]
                    outstack=[]
                    c=0
                    File = open("final.csv","w")
                    writeFirst = csv.writer(File)
                    rowval = ["Entry of Trace1","Exit of Trace1","Entry of Trace2", "Exit of Trace2"]
                    writeFirst.writerow(rowval)
                    File.close()

                    for i,line in enumerate(data):
                        if "Entry" in line:
                            if ">get" in line:
                                entry=line.split("Entry")
                                methodentry=entry[-1]
                                argument=methodentry.split(">")
                                argumententry=argument[-1]
                                instack.append(argumententry)
                        if "Exit" in line:
                            if "<get" in line:
                                exit=line.split("Exit")
                                methodexit=exit[-1]
                                outstack.append("Exit")
                                if(len(instack)!=0):
                                    self.listmethodentry2.append(instack.pop())
                                    self.listmethodexit2.append(outstack[-1])

                    f= open("result.txt","w+")
                    csvcontent = []
                    for i in range(len(self.listmethodexit1)):
                        csvcontent = [self.listmethodentry1[i],self.listmethodexit2[i],self.listmethodentry2[i],self.listmethodexit2[i],]
                        #filewriter.writerow([self.listmethodentry1[i],self.listmethodexit2[i],self.listmethodentry2[i],self.listmethodexit2[i]]) 
                        f.write(self.listmethodentry1[i]+"\t"+self.listmethodexit1[i]+"#"+self.listmethodentry2[i]+"#"+self.listmethodexit2[i]+"\n")       
                        with open("final.csv","a") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(csvcontent)
                            

                        #csvcontent.append([self.listmethodentry1[i]+self.listmethodexit2[i]+self.listmethodentry2[i]+self.listmethodexit2[i]])
                    f.close()
                    csvfile.close()
                    messagebox.showinfo(title=None, message='Xtrace files compared and stored in csv format')

                    #with open("final.csv","w+") as csvfile:
                    #    filewriter = csv.writer(csvfile,delimiter='|',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    #    filewriter.writerow(['Entry Trace1','Exit Trace1','Entry Trace2','Exit Trace2'])
                    #    for i in csvcontent:
                    #        filewriter.writerow(i)

                    #with open('reportfinal'+str(self.count)+'.csv','w') as finalcsv:
                    """for i in csvcontent:
                        with open('xTraceResults.csv', mode='w') as xTResults:
                            xResults = csv.writer(xTResults, delimiter='#', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            xResults.writerow(i)    """



if __name__ == '__main__':
    root=tk.Tk()
    file_browser = Browse(root, initialdir=r"E:\MATERIALS\python")
    file_browser.pack(fill='x', expand=True)
    root.mainloop()
