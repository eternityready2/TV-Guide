% rebase('admin/base.tpl')
<h1>On Demand Management</h1>
<style>
body {
    word-break: break-all;
}
.table-wrapper {
    margin: 30px auto;
    padding: 20px;	
}
.table-title {
    padding-bottom: 10px;
    margin: 0 0 10px;
}
.table-title h2 {
    margin: 6px 0 0;
    font-size: 22px;
}
.table-title .add-new i {
    margin-right: 4px;
}
table.table {
    table-layout: fixed;
}
table.table tr th, table.table tr td {
    border-color: #e9e9e9;
}
table.table th i {
    font-size: 13px;
    margin: 0 5px;
    cursor: pointer;
}
table.table th:last-child {
    width: 100px;
}
table.table td a {
    cursor: pointer;
    display: inline-block;
    margin: 0 5px;
    min-width: 24px;
}    
table.table td a.add {
    color: #27C46B;
}
table.table td a.edit {
    color: #FFC107;
}
table.table td a.delete {
    color: #E34724;
}
table.table td i {
    font-size: 19px;
}
table.table td a.add i {
    font-size: 24px;
    margin-right: -1px;
    position: relative;
    top: 3px;
}    
table.table .form-control {
    height: 32px;
    line-height: 32px;
    box-shadow: none;
    border-radius: 2px;
}
table.table .form-control.error {
    border-color: #f50000;
}
table.table td .add {
    display: none;
}
table.table td {
    overflow: hidden;
}
.channel-row {
    display: block;
    height: 0;
    overflow: hidden;
}
.channel-row.show {
    display:  table-row;
}
</style>

<div class="container-fluid">
    <div class="table-responsive">
        <div class="table-wrapper">
            <div class="table-title">
                <div class="row">
                    <div class="col-sm-8">
                        <h6>{{len(on_demand_data['channels'])}} channels</h6><input type="search" id="search" placeholder="Find channel" autocomplete="off"/>
                    </div>
                    <div class="col-sm-4">
                        <button type="button" onclick="onAddNew(event)" class="btn btn-outline add-new">Add New</button>
                        <button type="button" onclick="save(event)" class="btn btn-primary">Save all</button>
                    </div>
                </div>
            </div>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Image</th>
                        <th>Embed code</th>
                        <th>Category</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    % for channel in on_demand_data['channels']:
                        <tr class="channel-row show">
                            <td>{{channel['title']}}</td>
                            <td>{{channel['description']}}</td>
                            <td>{{channel['image']}}</td>
                            <td>{{channel['iframe']}}</td>
                            <td>{{channel['category']}}</td>
                            <td>
                                <a class="add" onclick="onAdd(event)" title="Add" >Add</a>
                                <a class="edit" onclick="onEdit(event)" title="Edit" >Edit</a>
                                <a class="delete" title="Delete" >Delete</a>
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
        </div>
    </div>
</div>  

<script>


$(document).ready(function(){
	$(document).on("click", ".delete", function(){
        $(this).parents("tr").remove();
		$(".add-new").removeAttr("disabled");
    });
});
    const REQUIRED_INDEXES = [0, 4]


    const actionsHtml = `
        <a class="add" onclick="onAdd(event)" >Add</a>
        <a class="edit"  onclick="onEdit(event)" title="Edit" >Edit</a>
        <a class="delete" title="Delete" >Delete</a>`;

    function onAddNew(e) {
        const table = document.querySelector('table tbody')
        const addNewBtn = e.target
        addNewBtn.disabled = 'disabled'
        const rows = document.querySelectorAll('table tbody tr')
        const newRowIndex = rows.length
        const newRowEl = document.createElement('tr')
        newRowEl.innerHTML = `
            <td><input type="text" class="form-control" name="title" id="title"></td>
            <td><input type="text" class="form-control" name="description" id="description"></td>
            <td><input type="file" onchange="onImgChange(event)" /><input type="hidden" class="form-control" name="image" id="image"></td>
            <td><input type="text" class="form-control" name="iframe" id="iframe"></td>
            <td><input type="text" class="form-control" name="category" id="category"></td>
			<td>${actionsHtml}</td>`
        table.append(newRowEl)
        const newAddBtn = newRowEl.querySelector('.add')
        const newEditBtn = newRowEl.querySelector('.edit')
        const newDelBtn = newRowEl.querySelector('.delete')
        newAddBtn.style.display = 'block'
        newEditBtn.style.display = 'none'
        newDelBtn.style.display = 'block'
        setTimeout(() => {
            newRowEl.scrollIntoView({behavior: 'smooth'})
        }, 100);
    }

    function onAdd(e) {
        const addBtn = e.target
        const parentRowEl = addBtn.parentElement.parentElement
        const rowInputEls = parentRowEl.querySelectorAll('input')
        rowInputEls.forEach((inputEl, index) => {
            const value = inputEl.value
            if (REQUIRED_INDEXES.includes(index) && !value) {
                alert("Please fill title and category")
                throw new Error("Required elements are emty")
            }
        })
        rowInputEls.forEach((inputEl, index) => {
            const value = inputEl.value
            if (REQUIRED_INDEXES.includes(index) && !value) {
                alert("Please fill title and category")
                throw new Error("Required elements are empty")
            }
            const parentCellEl = inputEl.parentElement
            switch (inputEl.type) {
                case 'text':
                    parentCellEl.innerText = value
                    break
                case 'hidden':
                    parentCellEl.innerText = value
                    break
            }
        })
        const editBtn = parentRowEl.querySelector('.edit')
        const delBtn = parentRowEl.querySelector('.delete')
        const addNewBtn = document.querySelector('.add-new')
        addBtn.style.display = 'none'
        editBtn.style.display = 'block'
        delBtn.style.display = 'block'
        addNewBtn.disabled = false
    }

    function onEdit(e) {
        const imageColIndex = 2
        const editBtn = e.target
        const parentRowEl = editBtn.parentElement.parentElement
        const cellEls = parentRowEl.querySelectorAll('td')
        cellEls.forEach((cellEl, index) => {
            const value = cellEl.innerText
            if (index === cellEls.length - 1) {
                return
            } else if (index === imageColIndex) {
                cellEl.innerHTML = `
                    <input type="file" class="form-control" onchange="onImgChange(event)" >
                    <input type="hidden" class="form-control" value="${value}">
                    `
            } else {
                cellEl.innerHTML = `<input type="text" class="form-control" value="">`
                cellEl.querySelector('input').value = value

            }
        })
        const addBtn = parentRowEl.querySelector('.add')
        const addNewBtn = document.querySelector('.add-new')
        editBtn.style.display = 'none'
        addBtn.style.display = 'block'
        addNewBtn.disabled = 'disabled'
    }



function save() {
    if (!confirm("Are you sure?")) return
        
    const rows = document.querySelectorAll('table tr')
    const newChannels = []
    rows.forEach(function(row, index) {
        if (index === 0) return
        const title = row.children[0].innerText
        const description = row.children[1].innerText
        const image = row.children[2].innerText
        const iframe = row.children[3].innerText
        const category = row.children[4].innerText
        newChannels.push({
            title,
            description,
            image,
            iframe,
            category,
        })
    })
    const newFile = { data: {channels: newChannels} } 
    const bodyStr = JSON.stringify(newFile)

    $.ajax( {
        url: "/live-tv/admin/on-demand",
        data: bodyStr,
        method: "POST",
        contentType:"application/json; charset=utf-8",
        success: function ( ) {
            alert("Done!")
        },
        error: function(a,b,c) {
            alert("Server error")
        }
    } );
}


async function onImgChange(e) {
    const formData = new FormData()
    formData.append('file', e.target.files[0])

    const response = await fetch('/on-demand/upload', {
        method: 'POST',
        body: formData
    })
    const data = await response.json()

    const hiddenInput = e.target.nextElementSibling
    hiddenInput.value = data.filename
}


    function search(e) {
        const value = e.target.value.toLowerCase()
        const allChannels = document.querySelectorAll(".channel-row")
        allChannels.forEach(el => {
            if (el.children[0].innerText.toLowerCase().includes(value)) {
                el.classList.add("show")
            } else {
                el.classList.remove("show")
            }
        })
    
    }
    document.querySelector("#search").addEventListener('input', search)


</script>