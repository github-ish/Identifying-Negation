"""\
--------------------------------------------------------------------------------
    USE: python <PROGNAME> (options) keyfile response
    OPTIONS:
        -h : print this help message
		
        -s "sentence": Analyses the given sentence.
					  
        -n : specifies the code to use a file to get new list of negative words. 
        	File needs to be specified with -f option. This option needs to be accompanied with -f option
			
        -f File Name: specifies the file from where to list of negative words
		
        -l : specifies to use a file to read a list of sentences to anaylse. File needs to be
        	with -t option. This option needs to be accompanied with -t option.
        -t File Name: specifies the file containing the list of sentences 
    
    DATAFORMAT:
		Negative Word File List: words in one line seperated by a comma (',')
		Sentences File : Each sentence written in a new line


--------------------------------------------------------------------------------
"""

import sys, getopt
class CommandLine:
    def __init__(self):
    	self.negativeWords=0
    	self.sentence_flag=0
    	self.sentence=""
        opts, args = getopt.getopt(sys.argv[1:],'hs:nf:lt:')
        opts = dict(opts)

        if '-l' in opts:
        	self.sentence_flag=1
        	if '-t' in opts:
        		self.sentence_file=opts['-t']
        	else:
        		print >> sys.stderr, '\n*** ERROR: must specify a file for sentences ***'
        		self.printHelp()

        if '-h' in opts:
            self.printHelp()
        if '-s' in opts:
        	self.sentence = opts['-s']
        	if self.sentence==None:
        		print >> sys.stderr, '\n*** ERROR: must specify a sentence ***'
        		self.printHelp()

#else:
#			print >> sys.stderr, '\n*** ERROR: must specify a sentence ***'
#			self.printHelp()
        if '-n' in opts:
			self.negativeWords=1
			if '-f' in opts:
				self.negative_file=opts['-f']
			else:
				print >> sys.stderr, '\n*** ERROR: must specify a file for negative words ***'
				self.printHelp()
		#if self.sentence=="":
		#	print >> sys.stderr, '\n*** ERROR: must specify a file for negative words ***'
		#		self.printHelp()
		

        

    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print >> sys.stderr, help
        exit()
