#!/usr/bin/perl

print "Content-type: text/html\n\n";

#takes the email address as STDIN from the HTML form (this is different from the way the account one does it)
$email = <STDIN>;

#it comes as "email=jack@aol.com"
#so remove the "email=" part
$email =~ s/email=//g;

#converts the hex characters back to ASCII:
$email =~ s/%([\dA-Fa-f][\dA-Fa-f])/pack("C", hex ($1))/eg;

#sends the browser some HTML info
print <<HTML;
<html><title>User generated haikus</title>
<body bgcolor="#FF9900">
<font face="monospace" size="+1">
<style>
p
{
padding-left:50px;
}
</style>
HTML

#makes sure the email field isn't blank
if ($email eq "") {
	print "<P><H3><U><B>Error: you didn't enter an email address!</H3></U></B>";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/email_list.html'>go back</a>";
}
#makes sure the email address is a valid "user@domain.top_level_domain" format
elsif ($email =~ m/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/) {
	print "<div align='center'><H3><U>Thank you for entering your email address!\n";
	print "<B>Your email address:</B>\n<p>";
	use CGI;
	print CGI::escapeHTML("$email\n");
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/email_list.html'>go back</a>\n";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/passform.html'>log in</a>\n";
#appends the email address to a data file
	open(LIST, ">>email_list.dat");
	use CGI; #nullifies any HTML or JavaScript code
	print LIST CGI::escapeHTML("$email;\n");
	close (LIST);
}
#if the address was invalid, it tells the user
else {
	print "<div align='center'><H3><U>This is not a valid email address!\n";
	print "<B>Please enter a valid email address</B>\n";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/email_list.html'>go back</a>\n";
}

print <<HTML;
</font>
</body>
</html>
HTML
