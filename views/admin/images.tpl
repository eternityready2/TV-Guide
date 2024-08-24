% rebase('admin/base.tpl')
<h1>Image Management</h1>
<form class="form-inline" method="post" enctype="multipart/form-data">
<div class="input-group input-group-sm">
  <div class="mr-2">
    <select class="form-control" name="channel">
%for channel in channels['channels']:
        <option value="{{ channel['number'] }}">{{ channel['name'] }}</option>
%end
    </select>
  </div>
  <div class="custom-file mr-2">
    <input type="file" class="custom-file-input form-control" name="image">
    <label class="custom-file-label">Choose file</label>
  </div>
</div>
<button type="submit" class="btn btn-primary">Submit</button>
</form>
%if success:
<div class="alert alert-success mt-2" role="alert">
  Upload stored
</div>
%end
