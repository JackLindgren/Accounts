#!/usr/bin/perl

#this can be simplified a bit using certain things in Perl to make the printing of the HTML info simpler and more automated
#but the program would still work the same
#it's also possible to do all of this on one self-contained, self-validating CGI form, instead of importing the inputs from an HTML page


#outputs html info to tell the browser to display HTML
print "Content-type: text/html\n\n";

#I forget why you need the size_of_form_information but you do
# $form_info is the stuff that's imported from the HTML form (create_account.html)
#it arrives in an unbroken string: "username=jack&email=jack@jack.com&password=monkey&password=monkey"
$size_of_form_information=$ENV{'CONTENT_LENGTH'};
read (STDIN, $form_info, $size_of_form_information);

#removes the extraneous information in the input string and replaces it with colons for delimiting
$form_info =~ s/username=//g;
$form_info =~ s/&email=/:/g;
$form_info =~ s/&password=/:/g;

#converts any hex characters back to ASCII:
$form_info =~ s/%([\dA-Fa-f][\dA-Fa-f])/pack("C", hex ($1))/eg;

#splits into an array to test each field for valid input later
@words=split/:/, $form_info;

#encodes the password using a hash
$password=$words[2];

$key="Z8j3lK39n4"; #this can be anything
$encrypted = &encode($password);

sub encode{
my($result)=@_;
$result=($result ^ $key);
$result=pack("u",$result);
$result=unpack("H*",$result);
return $result;
}

#^tbh I don't really know exactly how that works, and it's a bad way of doing it anyway

# looks at the .dat file to see if the username that was input
# already exists in the file. if it does, it assigns it to $username
open(ACCT, "accounts.dat");
while(<ACCT>){
	$name=$words[0];
        $username = $_ if /$name/;
        $username =~ s/:[A-Za-z0-9]*//g;
        chomp($username);
}
close(ACCT);

#tells the browser some stuff it'll be printing
print <<HTML;
<html><title>Create an account</title>
<body bgcolor="#FF9900">
<font face="monospace" size="+1">
<style>
p
{
padding-left:50px;
}
</style>
HTML

#tests if any fields are blank
if ($words[0] eq "" || $words[1] eq "" || $words[2] eq "" || $words[3] eq "" || $words[2] ne $words[3]) {
	print "<P><H3><U><B>Error: you left a field blank or didn't enter the password the same both times!</H3></U></B>";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/create_account.html'>go back</a>";
}
#tests if the username is already in use
elsif ($name eq $username){
	print "<P><H3>Invalid username</H3>\n";
	print "<p>the username $username is already in use\n";
	print "<br>please select another username\n";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/create_account.html'>go back</a>";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/login.html'>log in</a>";
}

#should also add a test for a valid email address:
if (@words[1] !~ m/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/){	#standard regex for email addresses
	print "<div align='center'><H3><U>This is not a valid email address!\n";
	print "<B>Please enter a valid email address</B>\n";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/email_list.html'>go back</a>\n";
}

#assigns the data to the .dat
else {
#first it tells the user what their password and stuff is:
	print "<div align='center'><H3><U>Thank you!\n";
	print "<br>Your submssion was successful!</U></H3></div>\n";
	print "<B>Username and password:</B>\n<p>";
	use CGI; #the CGI::escapeHTML thing is to nullify certain characters so a bad actor can't inject malicious Javascript or HTML
	print CGI::escapeHTML("your username: @words[0]\n");
	print "<br>";
	print CGI::escapeHTML("your email address is: @words[1]\n");
	print "<br>";
	print CGI::escapeHTML("your password: @words[2]\n");
	print "<br>";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/create_account.html'>go back</a>\n";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/login.html'>log in</a>\n";
#then it appends the new info in username:password:email_address form to the data file
	open(ACCT, ">>accounts.dat");
	use CGI;
	print ACCT CGI::escapeHTML("$words[0]:$encrypted:$words[1]\n");
	close (ACCT);
#and it also adds their email address to the email address list, just 'cause
	open(LIST, ">>email_list.dat");
	use CGI;
	print LIST CGI::escapeHTML("$words[1];\n");
	close(LIST);
}

#wraps up the HTML
print <<HTML;
</font>
</body>
</html>
HTML
