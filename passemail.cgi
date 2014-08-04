#!/usr/bin/perl

print "Content-type: text/html\n\n";

#gets the input
$size_of_form_information=$ENV{'CONTENT_LENGTH'};
read (STDIN, $form_info, $size_of_form_information);

#removes the "password=" part from the input
$form_info =~ s/password=//g;

#converts hex to ascii (I think - right?) we don't actually need it here because the password is just alphabetical
#but if the password contained other characters (e.g. "monkey_pass!") we'd need this so it's here.
$form_info =~ s/%([\dA-Fa-f][\dA-Fa-f])/pack("C", hex ($1))/eg;

print <<HTML;
<html><title>email list</title>
<body bgcolor="#FF9900">
<font face="monospace" size="+1">
<style>
p
{
padding-left:50px;
}
</style>
HTML

#this just has a hardcoded password - wow - such secure; much password
#if it's all good then it reads us the contents of the email list data file with some formatting
if ($form_info eq "monkey") {
	open (EMAIL, "email_list.dat");
	while (<EMAIL>) {
		chomp;
		print "<p>$_\n";
	}
	close(EMAIL);
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/passform.html'>go back</a>";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/email_list.html'>enter an email address</a>";

}
#otherwise, tells you to go away
else {
	print "<p><h3><u>You entered an incorrect password</h3></u></p>";
	print "<p><a href='http://hills.ccsf.edu/~jlindgr1/passform.html'>go back</a>";
}

print <<HTML
</font>
</body>
</html>
HTML
