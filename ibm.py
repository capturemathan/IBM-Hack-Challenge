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

parsed=[]
parsedindex=[]
var_list=[]
class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)

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
        self.tempvar=tk.BooleanVar()

        self.texts=tk.StringVar()
        self.selected_methods=[]
        self.converted_texts=tk.StringVar()

        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.javaSourceFile = tk.Entry(self, textvariable=self.filepath)
        self.traceCsv1 = tk.Entry(self, textvariable=self.trace1path)
        self.traceCsv2 = tk.Entry(self, textvariable=self.trace2path)
        self.method_entry = tk.Entry(self, textvariable=self.method_path)

        self.depth_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)

        self._xtrace = tk.Button(self, text='Generate Xtrace/Method Trace',command=self.xtrace)
        self.m_trace = tk.Button(self, text='Generate Application trace', command=self.mtrace)
        self.fetch_methods = tk.Button(self, text='Fetch Methods', command=self.fetch_methods)
        self.checkbox=tk.Checkbutton(self)
        self.convertXtraceToReadable = tk.Button(self, text='Convert',command=self.convert)
        self.method_names = tk.Label(self, text="Enter the methods (*,w,methods of inbuilt java packages)")
        self.stack_depth = tk.Label(self,text='Set your StackTrace')
        self.test = tk.Button(self, text='test',command=self.helo)

        self.javaFileBrowse = tk.Button(self, text="Browse...", command=self.browse)
        self.traceCsv1Browse = tk.Button(self, text="Browse...", command=self.browse2)
        self.traceCsv2Browse = tk.Button(self, text="Browse...", command=self.browse3)

        self._parse = tk.Button(self, text='Parse',command=self.parse)
        self._compare = tk.Button(self, text='Compare',command=self.compare)


        self.TraceSummary = tk.Text(root, height=2, width=60)
        self.TraceSummary.pack(side=tk.LEFT,fill=tk.Y)
        self.Scrollbar=tk.Scrollbar(root)
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _display_widgets(self):
        self.javaSourceFile.pack(fill='x', expand=True)
        self.javaFileBrowse.pack(anchor='se',pady=5)
        self.method_names.pack(anchor='center',pady=10)
        self.method_entry.pack(expand=tk.YES, fill=tk.X)
        self.stack_depth.pack(anchor='center',pady=10)
        self.depth_slider.pack()
        self._xtrace.pack(anchor='center',padx=50,pady=10)
        self.convertXtraceToReadable.pack(anchor='center',padx=50,pady=10)
        self._parse.pack(anchor='center',padx=50,pady=10)

        self.traceCsv1.pack(fill='x', expand=True)
        self.traceCsv1Browse.pack(anchor='se',pady=5)
        self.traceCsv2.pack(fill='x', expand=True)
        self.traceCsv2Browse.pack(anchor='se',pady=10)
        self._compare.pack(anchor='center',padx=50,pady=10)

        self.fetch_methods.pack(anchor='center',padx=50,pady=10)
        self.m_trace.pack(anchor='center',padx=50)
        self.test.pack(anchor='center')

    def browse(self):
        self.x=fd.askopenfilename(initialdir=self._initaldir,filetypes=self._filetypes)        
        self.filepath.set(self.x)
        print(self.filepath)


    def browse2(self):
        self.trace1=fd.askopenfilename(initialdir=self._initaldir,filetypes=self._filetypes)
        self.trace1path.set(self.trace1)
        print(self.trace1)

    def browse3(self):
        self.trace2=fd.askopenfilename(initialdir=self._initaldir,filetypes=self._filetypes)
        self.trace2path.set(self.trace2)
        print(self.trace2)


    def xtrace(self):
        print("Xtrace generating.....")
        self.count=self.count+1
        self.methods=self.method_entry.get()
        self.depth_value=self.depth_slider.get()
        os.system('java -classpath '+self.x+' -Xtrace:methods='+str(self.methods)+',stackdepth='+str(self.depth_value)+',maximal=mt,output=traceout'+str(self.count)+'.trc')
        print("Xtrace generated")


    def helo(self):
        pass

    def fetch_methods(self):
        variable = tk.StringVar(self)
        variable.set("one")
        javafile=self.x
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
         
            self.checkbar=Checkbar(self,parsed)
            self.checkbar.pack()
            



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
        with open (javafile, "r") as myfile:
            data=myfile.readlines()
            index=[]
            methods=[]
            parsedindex=[]
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
                    parsed.append(i)
                    parsedindex.append(index[p])

            for i in parsedindex:
                for j in range(i,len(data)):
                    if "{" in data[j]:
                        openbracketindex.append(j)

    #openbracketindex=set(openbracketindex)

            for i in parsedindex:
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

            for i,line in enumerate(parsed):
                if "main" in line:
                    indexfound=i
                    output[parsedindex[indexfound]+1]+=main_initialize
                    main_initialize=""
                    break
            
            for i,x in enumerate(parsedindex):
                if(self.checkbar_state[i]==1):
                    self.selected_methods.append(i)
                    flag=0
                    for j in range(x,len(output)):
                        if "{" in output[j] and flag==0:
                            function_name='"'+output[x].strip()+'"'
                            entry_trace='Trace.trace( handle, 0,'+function_name+');'
                            output[j]+=(entry_trace)
                            flag=1

            self.selected_methods.sort()
            print(self.selected_methods)
            for j in self.selected_methods:
                for i,x in enumerate(closebracketindex):
                    if j==i:
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
     
    def convert(self):
        print('converting')
        os.system('java com.ibm.jvm.format.TraceFormat traceout'+str(self.count)+'.trc')

        with open('traceout'+str(self.count)+'.trc.fmt','rb') as f:
            self.converted_texts=f.read()
        

        self.TraceSummary.insert(tk.CURRENT,self.converted_texts)
        
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
