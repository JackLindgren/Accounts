#!/usr/bin/perl

print "Content-type: text/html\n\n";

#gets the input from the login.html page
$size_of_form_information=$ENV{'CONTENT_LENGTH'};
read (STDIN, $form_info, $size_of_form_information);

#removes the extraneous information in the input string and replaces with useful delimiters
$form_info =~ s/username=//g;
$form_info =~ s/&password=/:/g;

#converts any hex characters back to ASCII:
$form_info =~ s/%([\dA-Fa-f][\dA-Fa-f])/pack("C", hex ($1))/eg;

#splits into an array to test each field for valid input later
@words=split/:/, $form_info;

#encrypt the password that was just entered
#(figuring its better to encrypt the input, than to decrypt the one we're testing against)
$key="Z8j3lK39n4";
$encrypted = &encode($words[1]);

sub encode{
my($result)=@_;
$result=($result ^ $key);
$result=pack("u",$result);
$result=unpack("H*",$result);
return $result
}

open(ACCT, "accounts.dat");
while(<ACCT>){
	$name=$words[0]; #this is the username that was just entered
	$password = $_ if /$name/; #if the username is in the file, assign
					#that line to $password
	$password =~ s/$name://g; #remove the username part so $password is the encrypted password
	$password =~ s/:[A-Za-z0-9._%+-]+@[A-Za-z0-9._]+\.[A-Za-z]{2,4}$//; #removes the email address

}
close(ACCT);

print <<HTML;
<html><title>User generated haikus</title>
<body bgcolor="red">
<font face="monospace" size="+1">
<style>
p
{
padding-left:50px;
}
</style>
HTML

chop($password);

#if the password matches, then you're good and it logs you in and shows this message
#(ignore the commented out print statements - it's for a different version of the statement)
if ($encrypted eq $password) {
	print "<div align='center'><H3><U>Success!\n";
	print "<br>You are now logged in as @words[0]</U></H3></div>\n";
#	print "<B>Username and password:</B>\n<p>";
#	print "<br>password in yourfile: $password\n";
#	print "<br>password you entered: $encrypted\n";
	print "<br>";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/create_account.html'>go back</a>\n";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/login.html'>log in</a>\n";

#prints the content message
#reads this from another data file
#e.g. you could use this to read out the contents of the password file if you want, or the email list file
	open (MSG, "message.dat");
	while (<MSG>) {
		chomp;
		print "<p>$_\n";
	}

#prints the email list - I used to have it do this but I changed my mind but here's how you'd do it:
#        open (EMAIL, "email_list.dat");
#        while (<EMAIL>) {
#                chomp;
#                print "<p>$_\n";
#	}
}
#and if their stuff didn't match, then it tells them so (duh)
else {
	print "<P><H3><U><B>Error: this username and password do not match</H3></U></B>";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/login.html'>go back</a>";
}

print <<HTML;
</font>
</body>
</html>
HTML
