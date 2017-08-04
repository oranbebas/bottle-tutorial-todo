<p>The open items are as follows:</p>
<table border="1">
%for row in rows:
  <tr>
    <td>{{row[0]}}</td>
    <td>{{row[1]}}</td>
    <td><a href="/item{{row[0]}}">show</a></td>
    <td><a href="/edit/{{row[0]}}">edit</a></td>
  </tr>
%end
</table>

<a href="/new">create new task</a>
