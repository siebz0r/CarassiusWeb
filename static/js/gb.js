$("#signForm").submit(function(event) {

	event.preventDefault();

	var $form = $(this);
	var url = $form.attr("action");
	var message = $form.find('textarea[name="content"]').val();

	var posting = $.post(url, {
		content : message
	})

	posting.done(function(data) {
		$('#messages').html($(data).filter('#messages'));
		$('textarea[name="content"]').val('');
	})
})