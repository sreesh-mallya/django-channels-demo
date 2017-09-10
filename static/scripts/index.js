$('#error').hide();

$('#messages').animate({
    scrollTop: $("#messages").prop("scrollHeight")
}, 0);

function slugify(string) {
  return string
    .toString()
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^\w\-]+/g, "")
    .replace(/\-\-+/g, "-")
    .replace(/^-+/, "")
    .replace(/-+$/, "");
}

$('#room').on('submit', function(event) {
	event.preventDefault();
	var room = $('#channel_name').val();
	if(room === '') {
		window.location = "/new/";
	} else {
		window.location = slugify(room);
	}
});
