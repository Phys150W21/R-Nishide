# Setup Instructions 

Github can be used to backup your whole 150 directory, so that we can collaborate for debugging and analysis purposes. 

git is a computer language that works from a linux terminal. So this will make it easier to transfer code in and out of the pi, and to work together.


This also means you can copy code in and out of your github and into your pi. So you can write analysis scripts in whatever IDE you are used to, and then upload to your github, then pull that from your pi easily. 
## Important Features 

Repository: Collection of all your files and folders. Each person has a repository for themselves. 

Branch: A repository can be branched so that multiple people are working on code from the same origin. The branches can be merged so that changes are reflected in the "main" branch, or the origin.

Commit: Commit changes to code

Pull request: Ask collaborators to look at this code 

Patch: Change this part of code 

## To set up 

### First set up 
Please email me your github user-name if you want to use this so I can add you as a collaborator. 

First, from /home/pi/150 run (of course replacing with the url for you repository). You will probably need to provide authentification. 

<pre><code>git clone https://github.com/Phys150W21/FirstInitial-LastName
</code></pre>

Next, copy your 150 file into the new directory that you got by cloning. 

<pre><code>cp -r ./150 ./FirstInitial-LastName
</code></pre>

### Add code to online github from pi 

Now you have your git repo mirrored in your terminal. 

To add code to your git repo or update, copy your 150 folder into the git folder to make sure it is up to date. Then you will need to bring the git folder to the stage. Next you will push the specific file or files you want to update. Finally, you will commit the file. 
<pre><code>cp -r ./150 ./FirstInitial-LastName
git add ./FirstInitial-LastName
git commit -m ./my-file
git push origin main
</code></pre>

This will commit your file to main. Now your online github will have the code from your pi. 

### Get code from online github onto pi 

This is just the reverse. You can just reclone the whole github repo to update the git folder in your pi:

<pre><code>git clone https://github.com/Phys150W21/FirstInitial-LastName
</code></pre>

Now the code you collaborated on from the online github, or that you uploaded to your repo from an IDE is on your pi in the git folder. 

You can copy whatever specific code out of the git folder on the pi into your 150 folder. 

## Notes

Be careful about overwriting files. If you are editing a folder and debugging, it is a good idea to save the original file as a backup before making changes: 

<pre><code>cp file-to-edit.py file-to-edit-backup.py
</code></pre>

Github wil aslo save the versions of each file. 
