# macro/UserStoryIR.py 

def execute(macro, args): 

    done = float(args.split(',')[0]) 
    total = float(args.split(',')[1]) 

    unit = 2 
    left = total - done 
    completeness = int(float(done) / float(total) * 1000) / 10.0

    if completeness > 100:
        result = """
        <font color='#6495ED'>%(done)s</font><font color='#FF7A85'>%(over)s</font>
        """ % {'done':"l"*int(total+0.5), 'over':"l"*int(-(left)+0.5)}
    else:
        result = """
        <font color='#6495ED'>%(done)s</font><font color='#BEEFFF'>%(left)s</font>
        """ % {'done':"l" * int(done+0.5), 'left':"l"*int(left+0.5)}
    
    #macro.request.write("this is the macro " + macro.name + " with args:" + args)

    return """%s <small>%s/%s(%s%%)</small>""" % (result, done, total, completeness)
