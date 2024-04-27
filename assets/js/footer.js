function generateFooter() {
  var footer = document.getElementById("footer");
  if (footer) {
    footer.innerHTML = `
    <div class="bg-dark text-white pt-4 pb-3">
        <div class="container">
            <!-- Section: Links -->
            <section class="mt-5">
                <!-- Grid row-->
                <div class="row text-center d-flex justify-content-center pt-5">
                    <!-- Grid column -->
                    <div class="col-md-2">
                        <h6 class="text-uppercase font-weight-bold">
                            <a href="/about.html" class="text-white"></a>
                        </h6>
                    </div>
                    <!-- Grid column -->


                    <!-- Grid column -->
                    <div class="col-md-2">
                        <h6 class="text-uppercase font-weight-bold">
                            <a href="./help.html" class="text-white"></a>
                        </h6>
                    </div>
                    <!-- Grid column -->

                </div>
                <!-- Grid row-->
            </section>
            <!-- Section: Links -->

            <hr class="my-5" />


        </div>
        <!-- Grid container -->

        <!-- Copyright -->
        <div class="text-center p-3" style="background-color: none">
            © 2024 Copyright:
            <a class="text-white" href="https://blazeeh.github.io/ytb-vid/">https://blazeeh.github.io</a>
        </div>
    </div>
`;
  }
}
