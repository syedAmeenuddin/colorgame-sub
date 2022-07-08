let otpcount = 0;
$(document).ready(function () {
	$('.loader').hide();
	$('.login_button').on('click',function(){
		$('.loader').show();
	})
	$('.registerbtn').on('click',function(){
		$('.loader').show();
	})
	$('.forgotbtn').on('click',function(){
		$('.loader').show();
	})
	
	$('.DigitsOnly').keyup(function(){
		this.value = this.value.replace(/[^\d]/g,'');
	})
	$('.DigitsOnly').keydown(function(){
		this.value = this.value.replace(/[^\d]/g,'');
	})
	$('.AlphaOnly').keyup(function(){
		this.value = this.value.replace(/[^a-zA-Z \.]/g,'');
	})
	$('.AlphaOnly').keydown(function(){
		this.value = this.value.replace(/[^a-zA-Z \.]/g,'');
	})
	$('.AlphaNumericOnly').keyup(function(){
		this.value = this.value.replace(/[^0-9a-zA-Z \.]/g,'');
	})
	$('.AlphaNumericOnly').keydown(function(){
		this.value = this.value.replace(/[^0-9a-zA-Z \.]/g,'');
	})
	
    $('.btnSendOTP').on('click',function(){
		if($("#PhoneNumber").val() != "" && $("#PhoneNumber").val().length == 10)
		{
			$('.btnVerifyOTP').removeClass('disablediv');
			$('.btnSendOTP').prop('disabled',true);
			$('.btnSendOTP').addClass('disablediv');
			if (otpcount==0 || otpcount==1){
				otpcount+=1
				setTimeout(resendOTP, 60000);
				Android.SendVerificationCode('+91'+$("#PhoneNumber").val());
			}
			else{
				alert('try again after 24hrs!');
				$('.btnSendOTP').addClass('disablediv');
				$('.btnVerifyOTP').addClass('disablediv');
			}
		}
		else {
			alert('enter mobile number and mobile number should have 10 digits');
		 }
			function resendOTP(){
				if (otpcount==0 || otpcount==1){
				$('.btnSendOTP').removeClass('disablediv');
				$('.btnSendOTP').html('Resend OTP')
				$('.btnVerifyOTP').removeClass('disablediv');
				}else{
					$('.btnSendOTP').addClass('disablediv');
				}
			}
		
	});

	$('.btnVerifyOTP').on('click',function(){
		if($("#otp").val() != "" && $("#otp").val().length == 6)
		{
			otpcount=2;
			$('.btnSendOTP').addClass('disablediv');
			$('.btnVerifyOTP').addClass('disablediv');
			Android.verifyOTPCode($("#otp").val());
		}else{
			$('.btnVerifyOTP').removeClass('disablediv');
			alert('check entered OTP!');
		}
	});
	
	



})
function isVerified(val){
	console.log(val);
	if(val)
	{
		otpcount=2;
		$('#txtpassword').prop('disabled',false);
		$('#btnRegister').prop('disabled',false);
		$('.btnVerifyOTP').addClass('disablediv');
		$('.btnSendOTP').addClass('disablediv');
	}
	else
	{
		$('.btnVerifyOTP').removeClass('disablediv');
		$('#txtpassword').prop('disabled',true);
		$('#btnRegister').prop('disabled',true);
		alert('Invalid OTP')
	}
}
// function LoginValidateForm(){
// let _form = document.forms["form"];
// console.log(_form.mobilenumber.value.length)
// if (_form.mobilenumber.value.length!=10 || _form.password.value.length<8){
// 	alert('mobile number should have 10 digits and password should have more than 8 characters');
// 	// return true;
// }
// }