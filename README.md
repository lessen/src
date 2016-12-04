[home](http://tiny.cc/ttv1) |
[copyright](https://github.com/ttv1/src/blob/master/LICENSE.md) &copy;2016, tim&commat;menzies.us
<br>
[<img width=900 src="https://github.com/ttv1/src/blob/master/img/banner.png?raw=true">](http://tiny.cc/ttv1)<br>
[src](https://github.com/ttv1/src) |
[chat](https://ttv1.slack.com/)

______


# Home page

<table border=0 align=center>
<tr>
<td align=center><b>News
<img width=300 src="img/200x1.png"></b>
</td>
<td align=center><b>Tutorials
<img width=100 src="img/200x1.png"></b>
</td>
<td><b>Workshops</b><img width=100 src="img/200x1.png"/></b>
</td>
<td align=center><b>Cool stuff
<img width=100 src="img/200x1.png"></b>
</td>

</tr>
<tr>
<td align=center><img src="img/news.png">
</td>  

     <td align=center><img src="img/lectures.gif">
     </td><td align=center><img src="img/review.gif">
     </td><td align=center><img width=64 src="img/books.png">
     </td> </tr>
     <tr>
     <td valign=top  xwidth="100px">

     </td>
     <td valign=top  xwidth="100px">
   </td><td valign=top xwidth="100px">
     </td><td valign=top>

     </td>
</tr></table>

Goals: this code is  a reference implementation of the ideas in my talk 
[Data Science<sup>2</sup>  = (Test * DataScience)](http://tiny.cc/timm4). This is 
 a combined data mining/optimization tool kit that is

- *Fast*: 
      - All algorithms near linear-time, not RAM hogs;
- *Light*: 
      - Small memory footprint;
- *Goal aware*: 
      - Mulitple goals = no problem, different goals = different models;
- *Explicable*:
      - Can offer a succinct human-understandable presentation of waht it has learned;
- *Actionable*:
      - Comments not just on _what is_ but also _what to do_ (and when we say "what" and "do", those statements understand
        local practicalities like what is observable and what is controllable);
- *Humble*: 
      - Offers a <em>cerfication envelope</em> where all conclusions come with a note saying 
        "you should (not) trust me since I have (not) seen this kind of thing before";
- *Context-aware*: 
       - Knows how local parts of the data can lead to different models; knows how to find different contexts;
- *Sharable*: 
       - Knows how to transfer models/data between contexts;
- *Privacy-aware*: 
       - Can hid data from individuals while preserving trends in the whole population;
- *Self-tuning*: 
       - Can do so, very quickly;
- *Incremental*: 
       - Can update old models with new ideas.
 
That's "all". Should not take more than a few Ph.D.s to finish. 
