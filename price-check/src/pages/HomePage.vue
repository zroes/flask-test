<template>
  <form @submit.stop="sendQuery()">
    <h3>Enter a search query:</h3>
    <input type="text" v-model="editable.query">
    <button>Submit</button>
  </form>
  <p>Note: this may take up to 10 seconds</p>

  <div class="container-fluid">
    <div class="row">
      <div v-for="result in results" class="col-3">
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
      async sendQuery() {
        const query = editable.value.query
        const searchParams = {
          "query": query,
          "includes": {
            "tj": true,
            "ab": true,
            "fm": true,
            "wf": true,
            "sf": false,
            "tc": false
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
  width: 100%;
  max-height: 20vh;
}
</style>
