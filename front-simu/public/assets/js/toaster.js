class Toaster {
    constructor() {
        this.toaster = document.createElement("div");
        this.toaster.id = "toaster";
        document.body.appendChild(this.toaster);
    }

    showToast(message, type) {
        const toasterMessage = document.createElement("div");
        toasterMessage.classList.add("toaster-message");

        if (type === "info") {
            toasterMessage.classList.add("info");
        } else if (type === "warning") {
            toasterMessage.classList.add("warning");
        } else if (type === "error") {
            toasterMessage.classList.add("error");
        }

        toasterMessage.innerText = message;
        this.toaster.appendChild(toasterMessage);

        setTimeout(() => {
            toasterMessage.style.opacity = 0;
            setTimeout(() => {
                this.toaster.removeChild(toasterMessage);
            }, 500); 
        }, 3000);
    }

    error(message) {
        this.showToast(message, "error");
    }

    warning(message) {
        this.showToast(message, "warning");
    }

    info(message) {
        this.showToast(message, "info");
    }
}


export const toaster = new Toaster()