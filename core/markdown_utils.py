
def paragraph(text):
    return '<p>' + text + '</p>'

def h1(text):
    return '<h1>' + text + '</h1>'

def h2(text):
    return '<h2>' + text + '</h2>'

def h3(text):
    return '<h3>' + text + '</h3>'

def h4(text):
    return '<h4>' + text + '</h4>'

def h5(text):
    return '<h5>' + text + '</h5>'

def h6(text):
    return '<h6>' + text + '</h6>'

def link(text, url):
    return '<a href="' + url + '">' + text + '</a>'

def bold(text):
    return '<b>' + text + '</b>'

def italic(text):
    return '<i>' + text + '</i>'

def author(text):
    return '<span>' + italic("-Added by: " + bold(text)) +'</span>'

def list_item(body,auth):
    return '<li>' + body + author(auth) + '</li>' + '\n'



