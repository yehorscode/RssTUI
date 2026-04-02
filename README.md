# RssTUI - RSS protocol inside your terminal

This is made for Summer of Making 2025! rss reader app for your terminal

## Table of Contents

-   [Quick Start](#-quick-start)
-   [What is this & How it's made](#what-is-this--how-its-made)
    -   [Idea](#idea)
    -   [How it's made](#how-its-made)
    -   [What is this](#what-is-this)
-   [Installation](#installation)
    -   [Easy Installation from PyPI (Recommended)](#easy-installation-from-pypi-recommended)
    -   [Development Installation](#development-installation)
    -   [Linux! (tested, works 100%)](#linux-tested-works-100)
    -   [Windows (not fully tested)](#windows-not-fully-tested)
    -   [MacOS](#macos)
    -   [Running](#running)
-   [Please vote for me!!](#please-vote-for-me)

## What is this & How it's made

### Idea

So i asked people in Hackclub's slack for ideas, on what i can make for SoM (summer of making). And Youssef gave an idea to make an app with Textual. So here i am!

### How it's made

The project uses Python 3.11.4, Textual and a Venv python virtual enviroment

Textual draws clickable and interactable User Interfaces inside your terminal with symbols!
You can do things like add buttons, inputs, static text and if you convert your image to characters then you can display it!
Learn more on Textual wiki: https://textual.textualize.io/

### Inner workings

_And i wonder, if you know..._ how it works! - _probably kanye east_

As i said previously, i use Textual. It's really a great library. But some feeds return HTML content. And as you have guessed: it isn't easibly readable for us humans, and we arent horses, we are humans.

So how do i go around this? Well it's actually pretty easy (if you don't count in regex i hate regex with all of my hearth)
I just use the `html2text` library! Then i can write pretty simple (again not counting regex) methods to parse html into pretty text

First we need to write a main class for html parsing, it initiates the parser and says what to parse, heres it:

```python
class ParseHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_tag = False

    def handle_starttag(self, tag, attrs):
        if tag in ['br', 'p']:
            self.text.append('\n')
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.text.append('\n## ')
        elif tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.text.append(f'[')
                    break

    def handle_endtag(self, tag):
        if tag == 'a':
            self.text.append(']')
        elif tag in ['p', 'div']:
            self.text.append('\n')

    def handle_data(self, data):
        self.text.append(data.strip())

    def get_text(self):
        return ''.join(self.text)
```

Not much right? Yeah i think so
Now important thing is we ont use it directly, it just makes changes to the `HTMLParser` from `html`
We then use the `HTML2Text` in code from `html2text`. Now i dont really understand fully how this all works, classes are like dark magic for me. But they work!

### Why doesnt the app support images

Because it's a pain in the butt to do so. WHy? Images are big, like very big 1080x1920 pixel, that's 2073600 in total!!!!!
And the terminal (textual library) can draw pixels as text or unicode color blobs or something i dont remember honestly. all of what i say may be wrong so dont really use what i say as a guide okay?
So to draw an image we need a lot of pixels, that we dont have. Now there are workorounds but theyr hard to do etc etc. I can always convert an image to be 40x40 pixels which is much smaller, but that means we lose all the details and probably you wouldn't be even able to recognise what it was before pixelifying

### What type of feed can i add?
A rss feed, any rss feed. as long as it doesnt use [buss:// protocol or something](https://youtu.be/qiOtinFFfk8?si=iK7dqXbvJcF0ulY5)
It can have HTML inside it, but only basic nothing crazy. Yeah that's about it

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

# Installation

## Easy Installation from PyPI (Recommended)

PyPi is a great service to host python scripts and packages. Here's how to install it:

First u need to create some sort of folder for my app and activate the venv

```bash
mkdir rsstui
```

Then activate env

```bash
python3 -m venv venv
```

And

```bash
source venv/bin/activate
```

Note: If u use fish then add `.fish` to the end of the command so it looks like: `source venv/bin/activate.fish`

Now there's easy part

```bash
pip install rsstui
```

And then run

```bash
rsstui
```

Congrtats u so smart

## Development Installation

Want to contribute or run from source? Here's how:

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
python3 rsstui/app.py
```

## Windows (not fully tested)

Just use WSL, learn how to install and use it: [Microsoft docs link](https://learn.microsoft.com/en-us/windows/wsl/install)
For using it inside wsl PLEASE use Windows Terminal and not cmd or powershell consoles. Wundows Terminal is a standalone app but it works a lot better then the other ones + looks very cool see [microsoft windows terminal documentation](https://learn.microsoft.com/en-us/windows/terminal/install)

## MacOS

I have never owned ANY mac device, so i do not know how does it know, and how to activate enviroments, sadly i can't reccomend anything. BUT BUT BUT the Linux methods may work. Please try them! Use bash methods
In theory mac os and linux both use unix, so installing the app should work right out of the box and maybe even with the auto installer

### Running

If installed via PyPi just run

```bash
rsstui
```

If u did it with the manual masochist method do:

```bash
python3 rsstui/app.py
```

Simple and clean! 🚀

# Please vote for me!!

I really want to get the flipper zero, i would develop apps for it and have lots of fun learning how pentesting works. Thanks! If u have issues just find me
