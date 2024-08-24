% rebase('admin/base.tpl')
<h1>Channel Management</h1>
%if success:
<div class="alert alert-success mb-2" role="alert">
  Channels stored
</div>
%end
<form class="form-inline" method="post">
<textarea name="channels" class="form-control" style="min-width: 100%;" rows="30">
{{ channels }}
</textarea>
<button type="submit" class="btn btn-primary btn-lg btn-block">Submit</button>
</form>

<script>
$('form').on('submit', function() {
    try {
        var obj = JSON.parse($('textarea').val());
    }
    catch (e) {
        alert(e)
        return false;
    }
})
</script>
