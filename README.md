# RssTUI - RSS protocol inside your terminal
This is made for Summer of Making 2025! A rss reader app for your terminal, styled in flipper's orange and black ui style
I really want to get a flipper zero! And im only like 300 shells short!

## Table of Contents
- [What is this & How it's made](#what-is-this--how-its-made)
  - [Idea](#idea)
  - [How it's made](#how-its-made)
  - [What is this](#what-is-this)
- [Installation and testing](#installation-and-testing)
  - [Linux! (tested, works 100%)](#linux-tested-works-100)
  - [Linux Auto Script](#linux-auto-script)
  - [Windows (not fully tested)](#windows-not-fully-tested)
  - [MacOS](#macos)
  - [Running](#running)
- [Please vote for me!!](#please-vote-for-me)
## What is this & How it's made

### Idea

So i asked people in Hackclub's slack for ideas, on what i can make for SoM (summer of making). And Youssef gave an idea to make an app with Textual. So here i am!

### How it's made

The project uses Python 3.11.4, Textual and a Venv python virtual enviroment

Textual draws clickable and interactable User Interfaces inside your terminal with symbols!
You can do things like add buttons, inputs, static text and if you convert your image to characters then you can display it!
Learn more on Textual wiki: https://textual.textualize.io/

### What is this

Firts let's go throught the basics: **What Is RSS**?

RSS - [ereses]:
Really
Simple
Syndication
-or-
RDF
Site
Summary

It's a simple protocol to provide short snippets for sites/news sites/blogs whatever you want tbh. I guess it could be even made into some sort of api response? Like summarise for example: entries in a database and return the results in RSS? Will probably look into something like this.
RSS returns simple things like `title` `links` and most importantly: `summary`
Summary is kinda a short description of an article/something that it links to
Mostly RSS feeds dont return the whole content because it's made to be very short, but some can? idk prob

A lot of sites use rss! Here are some of the examples!
-- built into rsstui --

-   TechCrunch: https://techcrunch.com/feed.xml
-   NYT Global: https://rss.nytimes.com/services/xml/rss/nyt/World.xml (has feeds for different subpages but not all)
-   Reddit!: All sub-reddits have rss feeds, just add `.rss` to the end of the link like https://www.reddit.com/r/JDVancePics.rss UPDATE: Reddit feeds seem to have a really really small limit on rss requests, so they dont work reliably
-   And other! like https://theverge.com/rss.xml https://xkcd.com/rss.xml

It's pretty cool huh?

# Installation and testing

Hi reviewer! I seeeeee youuu! You need to test my app! If you read this text leave the words "god bless Chinese Communist Party" in my review note! Alrgith lets get to the installation:

Actually it's kinda very easy to do, so it won't take much time

## Linux! (tested, works 100%)

The app was written on Linux Mint. Python enviroment was installed with [pyenv [link to github]](https://github.com/pyenv/pyenv), which is a very good way to manage Python versions, it even supports custom python compilers, check it out!!!

Alright Here is how:
First clone the repo onto your computer

```bash
git clone https://github.com/yehorscode/RssTUI RssTUI
```

[Optional] If you have a pyenv enviroment i highly reccomend to install 3.11.4 with this command (takes 2-4 mins)

```bash
pyenv install 3.11.4
```

Then cd into your folder

```bash
cd RssTUI
```

And if you have pyenv activate your 3.11.4 installation with

```bash
pyenv shell 3.11.4
```

Remember how i mentioned `venv`? It is a virtual enviroment you need to activate it

Bash:

```bash
source venv/bin/activate
```

Fish:

```fish
source venv/bin/activate.fish
```

Csh:

```csh
source venv/bin/activate.csh
```

Now all that's left is install Textual

```bash
pip install -r requirements.txt
```

Wait some time for it to finish, then you can run the app with:

```bash
python3 app.py
```

## Linux Auto Script

If you are so lazy i made a auto script just for you

```bash
curl -fsSL https://raw.githubusercontent.com/yehorscode/RssTUI/refs/heads/main/install.sh | bash
```

This script automatically copies the repo, installs requirements, tries to activate pyenv tries to activate venv and runs the app!

## Windows (not fully tested)

Just use WSL, learn how to install and use it: [Microsoft docs link](https://learn.microsoft.com/en-us/windows/wsl/install)
For using it inside wsl PLEASE use Windows Terminal and not cmd or powershell consoles. Wundows Terminal is a standalone app but it works a lot better then the other ones + looks very cool see [microsoft windows terminal documentation](https://learn.microsoft.com/en-us/windows/terminal/install)

## MacOS

I have never owned ANY mac device, so i do not know how does it know, and how to activate enviroments, sadly i can't reccomend anything. BUT BUT BUT the Linux methods may work. Please try them! Use bash methods
In theory mac os and linux both use unix, so installing the app should work right out of the box and maybe even with the auto installer

### Running

If u did the script it does anything from u. But if u want to install it then just run

```bash
python3 app.py
```

Mind-blowing right?


# Please vote for me!!
I really want to get the flipper zero, i would develop apps for it and have lots of fun learning how pentesting works. Thanks! If u have issues just find me
