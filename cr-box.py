from __future__ import print_function
import optparse
import os
import subprocess

def CreateVmailDirectory(domain,name):
    dir_domain="/var/vmail/"+domain
    dir_user=dir_domain+'/'+name
    try :
        if not os.path.isdir(dir_domain):
            os.system('su -c "mkdir ' +dir_domain+'" vmail')
            print ("Created domain's directory : ",dir)
        if os.path.isdir(dir_user):
            print("WARNING :\n The user`s directory is exist!!!\n ....\nMay be user ",name," is exist !!!")
            return 0
        os.system('su -c "mkdir '+dir_user+'" vmail')
        print("Created mailbox's directory: ", dir_user)
    except OSError:
        print("Error!!! Can't create Directory")
        return 0
    return 1

def CreateEmail(name,password,domain):
    proc_cr=subprocess.Popen(["/usr/bin/doveadm", 'pw', '-p', password,'-s','CRYPT'],stdout=subprocess.PIPE)

    crypt_pass=proc_cr.stdout.read().strip('\n')
    user_str=name+'@'+domain+':'+crypt_pass+':120:120:/var/vmail/'+domain+'/'+name+'::'
    try:
        f_users=open('/etc/dovecot/users','a')
        f_users.writelines(user_str)
        f_users.close()
        print("Created a new mailbox ",name)
        print("Created string is ", user_str)
    except IOError:
        print("Not access to add user")
        return 0
    return 1









def mainf():
    p=optparse.OptionParser()
    p.add_option('--name','-n')
    p.add_option('--password','-p')
    p.add_option('--domain','-d')
    options,arguments=p.parse_args()
    if not options.name  or not options.password or not options.domain:
        p.error('Not required parameters')
    #print('Name ',options.name,' Password ',options.password)
    if CreateVmailDirectory(options.domain,options.name):
        if CreateEmail(options.name,options.password,options.domain):
            return 0
    return 2222




if __name__=="__main__":
    mainf()
