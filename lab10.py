import math,numpy,random,sys

# test huffman code builder
def test_huffman(huffman,plist,expected_sizes,verbose=True):
    encoding_dict,tree = huffman(plist)

    if verbose:
        codes = [(code,symbol) for symbol,code in encoding_dict.items()]
        codes.sort()
        print('Huffman encoding:')
        avg_len = 0.0
        info_content = 0.0
        for code,symbol in codes:
            print ('  ',symbol,'=',"".join(map(str,code)) )
            for prob,s in plist:
                if s == symbol:
                    avg_len += len(code)*prob
                    info_content += prob*math.log(1.0/prob,2)
        print ("  Expected length of encoding a choice = %3.2f bits" %avg_len)
        print ("  Information content in a choice = %3.2f bits" % info_content)

    # make sure each code is unique
    codes = list(encoding_dict.values())
    for i in range(len(codes)):
        assert not codes[i] in codes[i+1:],\
               "Code %s appears more than once" % str(codes[i])

    # check expected sizes of encodings
    for expected,symbol in expected_sizes:
        got = len(encoding_dict[symbol])
        assert got==expected,\
               "For symbol %s: expected size %d, got %d" % (symbol,expected,got)

    return True

# verify huffman tree builder
def verify_task1(huffman):
    # test case 1: four symbols with equal probability
    test_huffman(huffman,
                 # symbol probabilities
                 ((0.25,'A'),(0.25,'B'),(0.25,'C'),
                  (0.25,'D')),
                 # expected encoding lengths
                 ((2,'A'),(2,'B'),(2,'C'),(2,'D')),
                 verbose=False)

    # test case 2: example from section 22.3 in notes
    test_huffman(huffman,
                 # symbol probabilities
                 ((0.34,'A'),(0.5,'B'),(0.08,'C'),
                  (0.08,'D')),
                 # expected encoding lengths
                 ((2,'A'),(1,'B'),(3,'C'),(3,'D')),
                 verbose=False)

    # test case 3: example from Exercise 5 in notes
    test_huffman(huffman,
                 # symbol probabilities
                 ((0.07,'I'),(0.23,'II'),(0.07,'III'),
                  (0.38,'VI'),(0.13,'X'),(0.12,'XVI')),
                 # expected encoding lengths
                 ((4,'I'),(3,'II'),(4,'III'),
                  (1,'VI'),(3,'X'),(3,'XVI')),
                 verbose=False)

    # test case 4: 3 flips of unfair coin
    phead = 0.9
    plist = []
    for flip1 in ('H','T'):
        p1 = phead if flip1 == 'H' else 1-phead
        for flip2 in ('H','T'):
            p2 = phead if flip2 == 'H' else 1-phead
            for flip3 in ('H','T'):
                p3 = phead if flip3 == 'H' else 1-phead
                plist.append((p1*p2*p3,flip1+flip2+flip3))
    expected_sizes = ((1,'HHH'),(3,'HTH'),(5,'TTT'))
    test_huffman(huffman,plist,expected_sizes,verbose=False)

    # all tests passed: 1 point
    return 1

def verify_task2(decode,cdict,tree):
    message = [random.choice('ABCD') for i in range(100)]
    encoded_message = encode(cdict,message)
    decoded_message = decode(tree,encoded_message)
    assert message == decoded_message, \
           "Decoding failed: expected %s, got %s" % \
           (message,decoded_message)

    # test passed: 1 point
    return 1

# given sequence of objects
# return list of tuples (probability,objects)
# range is list of possible objects or None
def histogram(seq,range=None):
    counts = {}
    if range is not None:
        for r in range: counts[r] = 0
    for v in seq:
        if range is not None:
            assert counts.has_key(v),"histogram: value not in specified range "+str(v)
        counts[v] = counts.get(v,0) + 1
    l = float(len(seq))
    result = [(v/l,k) for k,v in counts.items()]
    result.sort()   # sort by probability
    result.reverse()  # highest probability first
    return result

def encode(encoding_dict,message):
    return numpy.concatenate([encoding_dict[obj] for obj in message])

# convert PNG image to vector of black-and-white pixels
# return (nrows,ncols,pixels)
def img2pixels(img,threshold = 0.5):
    if len(img.shape) == 2:
        # already a grey-scale image
        nrows, ncols = img.shape
        y = numpy.reshape(img,-1)
    else:
        nrows, ncols, pixel = img.shape
        if pixel == 3:
            # rgb image
            rgb2y = numpy.array([[.299],[.587],[.114]])
            x = numpy.reshape(img,(-1,3))
        elif pixel == 4:
            # rgba image
            rgb2y = numpy.array([[.299],[.587],[.114],[0]])
            x = numpy.reshape(img,(-1,4))
        y = numpy.reshape(numpy.dot(x,rgb2y),-1)

    # use threshold to get vector of black/white pixels
    bw = (numpy.reshape(y,-1) >= threshold) * 1

    return (nrows,ncols,bw)

# convert vector of black-and-white pixels to RGB array for imshow
def pixels2img(pixels,nrows,ncols):
    assert len(pixels)==nrows*ncols,"pixels2img: size of pixels not nrows*ncols"
    result = numpy.zeros((nrows*ncols,3),dtype=float)
    white = numpy.array([1.,1.,1.])
    for i in range(nrows*ncols):
        if pixels[i]: result[i,:] = white
    return numpy.reshape(result,(nrows,ncols,3))

# convert pixel vector into run-length vector
def pixels2runs(bw,maxrun=2**31):
    result = numpy.zeros(bw.size/2,dtype=int)  # worst case: alternating pixels
    index = 0
    color = 1
    run = 0
    for i in range(bw.size):
        if bw[i] == color:
            # extend length of run
            run += 1
        else:
            # end of run, save its length
            while run > maxrun:
                result[index] = maxrun
                result[index+1] = 0
                index += 2
                run -= maxrun
            result[index] = run
            index += 1
            # we've just seen first pixel of next run
            color = 1 - color
            run = 1
    if run != 0:
        while run > maxrun:
            result[index] = maxrun
            result[index+1] = 0
            index += 2
            run -= maxrun
        result[index] = run
        index += 1

    # trim result to length ensuring an even number of runs
    if (index & 1) == 0: index += 1
    return result[:index+1]

def runs2pixels(runs,npixels):
    bw = numpy.zeros(npixels,dtype=int)
    index = 0
    color = 1
    for run in runs:
        bw[index:index+run] = color
        color = 1 - color
        index += run
    return bw

def pixels2blocks(bw,nrows,ncols,w,h):
    blocks_across = (ncols+w-1)/w
    blocks_down = (nrows+h-1)/h
    result = numpy.zeros(blocks_across*blocks_down,dtype=int)
    index = 0

    block = numpy.zeros(w*h,dtype=int)
    convert = numpy.array([2**i for i in range(w*h)],dtype=int)
    for i in range(0,nrows,h):
        for j in range(0,ncols,w):
            block.fill(0)  # clear block
            for k in range(h):
                r = i + k
                if r >= nrows: break;
                start = r*ncols+j
                width = min(w,ncols - j)
                block[k*w:k*w + width] = bw[start:start+width]
            result[index] = sum(block*convert)
            index += 1
    return result

def blocks2pixels(blocks,nrows,ncols,w,h):
    blocks_across = (ncols+w-1)/w
    blocks_down = (nrows+h-1)/h
    pixels = numpy.zeros((blocks_down*h,blocks_across*w),dtype=int)

    for i in range(blocks_down):
        for j in range(blocks_across):
            block = blocks[i*blocks_across + j]
            for r in range(h):
                for c in range(w):
                    pixels[i*h + r,j*w + c] = (block >> (r*w + c)) & 1

    return numpy.reshape(pixels[:nrows][:ncols],-1)

##################################################
##
## Code to submit task to server.  Do not change.
##
##################################################

# =============================================================================
# import Tkinter
# class Dialog(Tkinter.Toplevel):
#     def __init__(self, parent, title = None):
#         Tkinter.Toplevel.__init__(self, parent)
#         self.transient(parent)
#         if title: self.title(title)
#         self.parent = parent
# 
#         body = Tkinter.Frame(self)
#         self.initial_focus = self.body(body)
#         body.pack(padx=5, pady=5)
# 
#         self.buttonbox()
#         self.grab_set()
# 
#         if not self.initial_focus:
#             self.initial_focus = self
# 
#         self.protocol("WM_DELETE_WINDOW", self.cancel)
#         self.geometry("+%d+%d" % (parent.winfo_rootx()+50,parent.winfo_rooty()+50))
#         
#         self.initial_focus.focus_set()
#         self.wait_window(self)
# 
#     def body(self, master):
#         return None
# 
#     # add standard button box
#     def buttonbox(self):
#         box = Tkinter.Frame(self)
#         w = Tkinter.Button(box, text="Ok", width=10, command=self.ok, default=Tkinter.ACTIVE)
#         w.pack(side=Tkinter.LEFT, padx=5, pady=5)
#         box.pack()
#         
#     # standard button semantics
#     def ok(self, event=None):
#         if not self.validate():
#             self.initial_focus.focus_set() # put focus back
#             return
#         self.withdraw()
#         self.update_idletasks()
#         self.apply()
#         self.cancel()
#         
#     def cancel(self, event=None):
#         # put focus back to the parent window
#         self.parent.focus_set()
#         self.destroy()
#         
#     # command hooks
#     def validate(self):
#         return 1 # override
# 
#     def apply(self):
#         pass   # override
# 
# # ask user for Athena username and MIT ID
# class SubmitDialog(Dialog):
#     def __init__(self,parent,error=None,title = None):
#         self.error = error
#         self.athena_name = None
#         self.mit_id = None
#         Dialog.__init__(self,parent,title=title)
# 
#     def body(self, master):
#         row = 0
#         if self.error:
#             l = Tkinter.Label(master,text=self.error,
#                               anchor=Tkinter.W,justify=Tkinter.LEFT,fg="red")
#             l.grid(row=row,sticky=Tkinter.W,columnspan=2)
#             row += 1
#         Tkinter.Label(master, text="Athena username:").grid(row=row,sticky=Tkinter.E)
#         self.e1 = Tkinter.Entry(master)
#         self.e1.grid(row=row, column=1)
# 
#         row += 1
#         Tkinter.Label(master, text="MIT ID:").grid(row=row,sticky=Tkinter.E)
#         self.e2 = Tkinter.Entry(master)
#         self.e2.grid(row=row, column=1)
# 
#         return self.e1 # initial focus
# 
#     # add standard button box
#     def buttonbox(self):
#         box = Tkinter.Frame(self)
#         w = Tkinter.Button(box, text="Submit", width=10, command=self.ok,
#                            default=Tkinter.ACTIVE)
#         w.pack(side=Tkinter.LEFT, padx=5, pady=5)
#         w = Tkinter.Button(box, text="Cancel", width=10, command=self.cancel)
#         w.pack(side=Tkinter.LEFT, padx=5, pady=5)
#         box.pack()
#         
#     def apply(self):
#         self.athena_name = self.e1.get()
#         self.mit_id = self.e2.get()
# 
# # Let user know what server said
# class MessageDialog(Dialog):
#     def __init__(self, parent,message = '',title = None):
#         self.message = message
#         Dialog.__init__(self,parent,title=title)
# 
#     def body(self, master):
#         l = Tkinter.Label(master, text=self.message,anchor=Tkinter.W,justify=Tkinter.LEFT)
#         l.grid(row=0)
# 
# # return contents of file as a string
# def file_contents(fname):
#     # use universal mode to ensure cross-platform consistency in hash
#     f = open(fname,'U')
#     result = f.read()
#     f.close()
#     return result
# 
# import hashlib
# def digest(s):
#     m = hashlib.md5()
#     m.update(s)
#     return m.hexdigest()
# 
# # if verify(f) indicates points have been earned, submit results
# # to server if requested to do so
# import inspect,os,urllib,urllib2
# def checkoff(f,task='???',submit=True):
#     tasks = ('L10_1','10_2')
#     if task == 'L10_1':
#         points = verify_task1(f)
#     elif task == 'L10_2':
#         points = verify_task2(f[0],f[1],f[2])
#         f = f[0]
#     else:
#         raise ValueError("task must be one of %s" % ", ".join(tasks))
# 
#     if submit and points:
#         root = Tkinter.Tk(); #root.withdraw()
#         error = None
#         while submit:
#             sd = SubmitDialog(root,error=error,title="Submit Task %s?"%task)
#             if sd.athena_name:
#                 if isinstance(f,str): fname = os.path.abspath(f)
#                 else: fname = os.path.abspath(inspect.getsourcefile(f))
#                 post = {
#                     'user': sd.athena_name,
#                     'id': sd.mit_id,
#                     'task': task,
#                     'digest': digest(file_contents(os.path.abspath(inspect.getsourcefile(checkoff)))),
#                     'points': points,
#                     'filename': fname,
#                     'file': file_contents(fname)
#                     }
#                 try:
#                     response = urllib2.urlopen('http://scripts.mit.edu/~6.02/currentsemester/submit_task.cgi',
#                                                urllib.urlencode(post)).read()
#                 except Exception(e):
#                     response = 'Error\n'+str(e)
#                 if response.startswith('Error\n'):
#                     error = response[6:]
#                 else:
#                     MessageDialog(root,message=response,title='Submission response')
#                     break
#             else: break
# 
#         root.destroy()
# =============================================================================
