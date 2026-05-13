/*app/static/js/privacy-notice.js
Created by Anuki Kithara
Last modified: 13/05/2026

Privacy notice popup for the call page.
Shows users a privacy notice before a call starts.
Allows users to hide the notice on the same browser or device.
*/

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("privacyNoticeModal");
    const continueBtn = document.getElementById("privacyNoticeContinue");
    const dontShowAgain = document.getElementById("dontShowPrivacyNotice");

    if (!modal || !continueBtn || !dontShowAgain) {
        console.warn("Privacy notice modal elements were not found.");
        return;
    }

    const privacyAccepted =
        localStorage.getItem("signbridgePrivacyNoticeAccepted");

    if (privacyAccepted !== "true") {
        modal.classList.add("show");
        modal.setAttribute("aria-hidden", "false");
    }

    continueBtn.addEventListener("click", function () {
        if (dontShowAgain.checked) {
            localStorage.setItem(
                "signbridgePrivacyNoticeAccepted",
                "true"
            );
        }

        modal.classList.remove("show");
        modal.setAttribute("aria-hidden", "true");
    });
});