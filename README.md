## htmlmatch: Automatic data scraping

Suppose you have a page with a list of videos (videos.html), and you want to get all the videos:

```html
<html>
<head><title>Example</title></head>
<body>
<div class="video">
        <a href="watch?v=0001">Title first video</a><img src="preview1.jpg"/></div>
<div class="video">
        <a href="watch?v=0002">Title second video</a><img src="preview2.jpg"/></div>
<div class="video">
        <a href="watch?v=0003">Title third video</a><img src="preview3.jpg"/></div>
...
</body>
</html>
```

You can easily extract the data from this web page, creating an extraction template like this (template.html):

```html
<div class="video"><a href="watch?v=$code$">$title$</a><img src="$preview$"/></div>
```

Just put `$variable$` where you want. Now if you run the script against videos.html and template.html, you get the raw data:

```
claudio@laptop:~$ ./htmlmatch.py videos.html pattern.html
code: 0001
title: The first video
preview: preview1.jpg

code: 0002
title: The second video
preview: preview2.jpg

code: 0003
title: The third video
preview: preview3.jpg
```

You can easily access all these filed using the library as a function in your python code and iterating the list (of dictionaries) it gives you back. For example:

```python
videos_page = urllib2.urlopen("http://www.videos-website.com/")
pattern = open("pattern.html", "r")
matches = htmlmatch(videos_page, pattern)
for map in matches:
    for k, v in map.iteritems():
        print k, v
    print
```
