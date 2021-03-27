def graphic_letters(chart,df,analysis,xytext,fontsize):
    """
    chart: variable where the graphic is stored, usually chart = sns.barplot()
    df: data frame with statistic result where the letters are stored
    analysis: a string that indicates the result displayed in the graphic
    xytext: (x,y) position of the letters
    fontsize: font size
    """
    
    groupsletters = df[analysis][analysis + '-groups']
    
    pat={}
    i = 0
    for p in chart.patches:  # p is each rectangle of the bar chart 
        pat[i] = p  # pat is a dictionary where each bar location is saved
        i+=1

    j = 0
    for p in pat:
        label = groupsletters[j]  # the label change its value for each iteration
        chart.annotate(label,  # this is the text
                       (pat[j].get_x() + pat[j].get_width() / 2., pat[j].get_height()),  # this is the point to label
                       ha='left',  # horizontal alignment can be left, right or center
                       va='center', # vertical alignment can be left, right or center
                       fontsize=fontsize, color='black',
                       xytext=xytext,  # distance from text to points (x,y)
                       textcoords='offset points')  # how to position the text
        j+=1