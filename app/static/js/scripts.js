$(document).ready(function(){
	error = "";												
	$( "#sign-up" ).submit(function() {						
		if ($('#sign-up input[name=password]').val() != $('#sign-up input[name=password_confirm]').val())
		{
			error = "passwords must match!";
			$("#signup-errors").text(error);
			return false;
		}
		return true;
	});
});