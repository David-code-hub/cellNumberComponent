<template>
  <div class="bg-[#16264E] h-[100vh] w-full lg:p-10 p-3 relative">
    <div class="flex h-full justify-center">
      <div
        class="bg-white rounded-xl mx-auto h-fit my-auto z-10 lg:w-[700px] relative"
      >
        <div class="rounded-sm lg:p-10 p-3 py-10">
          <!--start fallback message: when error occurs while fetching data-->
          <div
            class="bg-red-600/30 rounded-md p-3 mb-3 flex gap-5 justify-between"
            v-if="refresh"
          >
            <p class="text-sm text-red-600">
              A small error occurred while loading the page,please refresh.
            </p>
            <button
              class="text-red-600 font-normal text-sm underline"
              @click="getCountries(), (refresh = false)"
            >
              Refresh
            </button>
          </div>
          <!--end fallback-->
          <label for="input-number" class="lg:text-4xl text-lg font-extrabold"
            >Phone Number
          </label>
          <p class="text-gray-600 mt-3 lg:text-md text-sm">
            Please enter your phone number to continue.
          </p>

          <div class="grid grid-cols-5 mt-7">
            <div
              class="h-full w-full lg:px-5 lg:py-5 px-3 py-3 my-auto bg-[#16264E] rounded-l-xl col-span-1 cursor-pointer"
              @click="openModel = true"
            >
              <div class="grid gap-2 grid-cols-2">
                <img
                  :src="phoneCode?.flag"
                  class="h-[25px] w-[25px] my-auto object-contain"
                />
                <p class="text-white lg:text-lg text-xs my-auto">
                  {{ phoneCode?.code }}
                </p>
              </div>
            </div>
            <div class="col-span-3">
              <input
                v-model="phoneNumber"
                class="h-full appearance-none border lg:text-lg text-sm w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                type="number"
                placeholder="Phone Number"
              />
            </div>

            <button
              @click="submit"
              :class="{
                'opacity-75 cursor-not-allowed pointer-events-none':
                  !phoneNumber.toString().length ||
                  phoneNumber.toString().length < 9 ||
                  phoneNumber.toString().length > 9,
              }"
              class="lg:px-5 lg:py-3 px-3 py-1 text-white bg-[#F78026] rounded-r-xl font-light lg:text-lg text-xs text-center"
            >
              Submit
            </button>
          </div>
          <p
            class="text-red-500 text-xs italic mt-1"
            v-if="
              phoneNumber.toString().length < 9 ||
              phoneNumber.toString().length > 9
            "
          >
            Please enter a valid phone number.
          </p>
        </div>
        <!--start loader : especially helpful for users with low internet speed-->
        <div
          v-if="loading"
          class="bg-black/60 bg-blend-multiply text-center flex justify-center absolute top-0 h-full w-full rounded-xl"
        >
          <p class="my-auto text-white lg:text-lg text-sm">Loading...</p>
        </div>
        <!--end loader-->
      </div>
    </div>
    <!--start model-->
    <div
      class="fixed left-0 top-0 flex h-full w-full items-center justify-center bg-black bg-opacity-50 lg:py-10 p-5 z-20"
      :class="{ hidden: !openModel }"
    >
      <div
        class="max-h-full w-full max-w-xl overflow-y-auto rounded-2xl bg-white"
      >
        <p
          class="ml-3 mt-3 text-xl text-gray-600 cursor-pointer"
          @click="openModel = false"
        >
          ESC
        </p>

        <div class="w-full">
          <div
            class="m-5 my-10 lg:max-w-[400px] max-w-full lg:p-0 p-10 mx-auto"
          >
            <div class="mb-8">
              <h1 class="mb-4 lg:text-3xl text-gl font-extrabold">
                Choose Country
              </h1>
            </div>
            <div>
              <input
                v-model="search"
                type="text"
                placeholder="Country Name"
                class="h-full appearance-none border rounded-xl text-xl w-full mb-3 py-3 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              />

              <div
                class="grid text-sm grid-cols-4 gap-2 my-3 cursor-pointer justify-between text-left"
              >
                <p class="text-black">Flag</p>
                <p class="text-black col-span-2">Country</p>
                <p class="text-black text-right">Code</p>
              </div>
              <hr />
              <div class="h-[300px] overflow-auto">
                <div
                  class="grid grid-cols-4 text-sm gap-2 my-3 cursor-pointer justify-between text-left"
                  v-for="(country,index) in allCountries.filter(
          (c:any) => c?.name?.common.toLowerCase().includes(search.toLowerCase())
        )"
                  :key="country?.name?.common"
                  :tabindex="index"
                  @click="selectCountry(country)"
                >
                  <img
                    :src="country?.flags?.svg"
                    class="h-[25px] w-[25px] my-auto object-contain"
                  />
                  <p class="text-black col-span-2">
                    {{ country?.name?.common }}
                  </p>
                  <p class="text-black text-right">
                    {{ country?.idd?.root + country?.idd?.suffixes[0] }}
                  </p>
                </div>
              </div>
              <p class="text-gray-600 text-xs italic mt-4">
                Use tab and tab+shift to move up and down list.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--end model-->
    <img
      src="@/assets/images/ratherchatblob.png"
      class="lg:h-[20rem] h-[15rem] w-fit object-contain lg:top-0 top-[-2em] right-0 absolute z-2"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

/**
 * ideally I'd want to have my model and loader in seperate files
 * so that I don't have a cluttered code experience, but I decided to have everthing in
 * one file this time due to time contraints
 */
interface selectedCountry {
  flag: string;
  code: string;
  countryName: string;
}

const phoneCode = ref<selectedCountry>();
const openModel = ref(false);
const phoneNumber = ref("");
const allCountries: any = ref([]); //add a ts interface
const search = ref("");
const loading = ref(false);
const refresh = ref(false);

//handle select county
function selectCountry(country: any) {
  phoneCode.value = {
    flag: country?.flags?.svg,
    code: country?.idd?.root + country?.idd?.suffixes[0],
    countryName: country?.name?.common,
  };
  openModel.value = false;
}
/*handle fetch country data, default South Africa
I initially wanted to add a search function that takes a countryName as a param, but decided to 
get all country data and use it as a single source of truth so that I don't end up having multiple 
endpoints retrieving data(makes is harder to manage)
*/
async function getCountries() {
  try {
    loading.value = true;
    const response = await fetch(
      "https://restcountries.com/v3.1/all/?fields=name,flags,idd"
    );
    allCountries.value = await response.json();

    //handle set rsa as default: getting south africa from the array of countries to set as default value
    let southAfrica = allCountries.value.filter(
      (country: any) => country?.name?.common === "South Africa"
    )[0];
    //storing rsa default values as object
    phoneCode.value = {
      flag: southAfrica.flags.svg,
      code: southAfrica.idd?.root + "" + southAfrica.idd?.suffixes[0],
      countryName: southAfrica.name?.common,
    };
  } catch (error) {
    console.error("Error while fetching countries :", error);
    refresh.value = true;
  } finally {
    loading.value = false;
  }
}

function submit() {
  alert(
    `Submitting phone number: "${
      phoneCode.value?.code.substring(1) + phoneNumber.value
    }"`
  );
}

onMounted(() => {
  getCountries();
  //use esc key to close model
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      openModel.value = false;
    }
  });
});
</script>
