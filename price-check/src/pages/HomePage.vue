<template>
  <form @submit.stop="sendQuery()">
    <h3>Enter a search query:</h3>
    <input type="text" v-model="editable.query">
    <div class="d-flex p-2">
      <div class="mx-2">
        <input type="checkbox" name="" id="includesTJ" v-model="editable.includesTJ">
        <label for="includesTJ" class="px-1">Trader Joe's</label>
      </div>
      <div class="mx-2">
        <input type="checkbox" name="" id="includesAB" v-model="editable.includesAB">
        <label for="includesAB" class="px-1">Albertsons</label>
      </div>
      <div class="mx-2">
        <input type="checkbox" name="" id="includesFM" v-model="editable.includesFM">
        <label for="includesFM" class="px-1">Fred Meyers</label>
      </div>
      <div class="mx-2">
        <input type="checkbox" name="" id="includesWF" v-model="editable.includesWF">
        <label for="includesWF" class="px-1">Whole Foods</label>
      </div>
      <div class="mx-2">
        <input type="checkbox" name="" id="includesSF" v-model="editable.includesSF">
        <label for="includesSF" class="px-1">Safeway</label>
      </div>
      <div class="mx-2">
        <input type="checkbox" name="" id="includesSF" v-model="editable.includesTC">
        <label for="includesSF" class="px-1">Town and Country</label>
      </div>

    </div>
    <button>Submit</button>
  </form>
  <p>Note: this may take up to 10 seconds</p>

  <div class="container-fluid">
    <div class="row">
      <div v-if="loading">
        loading...
      </div>
      <div v-for="result in results" class="col-3" v-else>
        <div class="p2">
          <img class="size-img" :src="result.imgURL" alt="">
          <h3>{{ result.name }}</h3>
          <h5>${{ result.price }} | {{ result.size }}</h5>
          <p>{{ result.store }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { computed, ref } from "vue"
import Pop from "../utils/Pop.js"
import { searchService } from "../services/SearchService.js"
import { AppState } from "../AppState.js"

export default {
  setup() {
    const editable = ref({})
    return {
      editable,
      results: computed(() => AppState.searchResults),
      loading: computed(() => AppState.loading),
      async sendQuery() {
        const query = editable.value.query
        const searchParams = {
          "query": query,
          "includes": {
            "tj": editable.value.includesTJ ? editable.value.includesTJ : false,
            "ab": editable.value.includesAB ? editable.value.includesAB : false,
            "fm": editable.value.includesFM ? editable.value.includesFM : false,
            "wf": editable.value.includesWF ? editable.value.includesWF : false,
            "sf": editable.value.includesSF ? editable.value.includesSF : false,
            "tc": editable.value.includesTC ? editable.value.includesTC : false
          }
        }
        try {
          await searchService.search(searchParams)
        } catch (error) {
          Pop.error(error)
        }
      }
    }
  }
}
</script>

<style scoped lang="scss">
.size-img {
  max-width: 100%;
  max-height: 20vh;
}
</style>
