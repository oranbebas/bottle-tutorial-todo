<p>Edit the task with ID = {{no}}:</p>
<form action="/edit/{{no}}" method="POST">
  <input type="text" size="100" maxlength="100" name="task" value="{{old[0]}}">
  <select name="status">
    <option>open</option>
    <option>closed</option>
  </select>
  <br>
  <input type="submit" name="save" value="save">
</form>

<a href="/todo">back to list</a>
