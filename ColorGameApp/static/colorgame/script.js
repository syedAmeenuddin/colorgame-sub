let otpcount = 0;
$(document).ready(function () {
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
			
			
			function resendOTP(){
				if (otpcount==0 || otpcount==1){
				$('.btnSendOTP').removeClass('disablediv');
				$('.btnSendOTP').html('Resend OTP')
				$('.btnVerifyOTP').removeClass('disablediv');
				}else{
					$('.btnSendOTP').addClass('disablediv');
				}
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