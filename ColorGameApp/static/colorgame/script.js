let otpcount = 0;
$(document).ready(function () {
		$('.loader').hide();

		if (parseInt(mobilenumber) !=''){
			$('#mobilenumber').val(parseInt(mobilenumber));
		}

		$('.showLoader').on('click',function(){
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

		function RH_number(){
			$('#mobilenumber').prop('disabled',false);
		}
		
		if (parseInt(otpsign) == 1){
			$('#mobilenumber').prop('disabled',true);
			$('.btnVerifyOTP').removeClass('disablediv');
			$('#btnSendOTP').prop('disabled',true);
			$('#btnSendOTP').addClass('disablediv');
			if (otpcount==0 || otpcount==1){
				otpcount+=1
				setTimeout(resendOTP, 60000);
				Android.SendVerificationCode('+91'+$("#mobilenumber").val());
			}
			else{
				alert('try again after 24hrs!');
				$('#btnSendOTP').addClass('disablediv');
				$('.btnVerifyOTP').addClass('disablediv');
			}
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

		$('.btnVerifyOTP').on('click',function(){
			if($("#otp").val() != "" && $("#otp").val().length == 6)
			{   
				$('.loader').show();
				otpcount=2;
				$('.btnSendOTP').addClass('disablediv');
				$('.btnVerifyOTP').addClass('disablediv');
				Android.verifyOTPCode($("#otp").val());
			}else{
				$('.btnVerifyOTP').removeClass('disablediv');
				alert('check entered OTP!');
			}
		});
		
	});

	
	
function showloader(){
	$('.loader').show();
}
function goBack() { 
	window.history.back();
  }
function isVerified(val){
	$('.loader').hide();
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