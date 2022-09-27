** THIS REPOSITORY HAS BEEN ARCHIVED **

IssueTracker is (c) 2009 Nicholas H.Tollervey
http://ntoll.org/contact

This small web-application is an exercise in using my workflow app. It was
written very quickly (in under 2 days) because I had a deadline: I wanted to
have it "finished" so I could demonstrate it to someone. As a result, important
stuff like unit tests are missing or partially complete. I'll add those in the 
coming days (although there are stubs for them).

Please note: this is a toy "demo" project and *not* for serious use. Any
feedback please contact me (see URL at the top of this file).

Quickstart guide:

1) git clone git://github.com/ntoll/IssueTracker.git
2) cd IssueTracker
3) git submodule init
4) git submodule update
5) ./manage.py syncdb (if you want to use the test examples answer 'no' when
asked about defining superusers)
6) ./manage.py loaddata project_test_data
7) ./email_server.sh &
8) ./manage.py runserver
9) Open you browser at http://localhost:8000/

If you executed step 6 then there are five users you can play with:

admin (the admin user - obviously)
alice 
bob
charlie
dave

All have the password 'password'

Obviously, you can also use Django's built in admin interface (log in as admin
if you've loaded the test examples):

http://localhost:8000/admin/

If you have GraphViz installed properly (see: http://www.graphviz.org/) then
make sure the GRAPHVIZ_DOT_COMMAND constant in settings.py points to the correct
command. You should then be able to see visualisations of the workflows. For 
example:

http://localhost:8000/workflow/feature_request_handler.png

(If you have the test examples loaded - the filename is the workflow's slug
field)

As always, comments, suggestions and feedback most welcome.
