import { AppState } from "../AppState.js"
import { Result } from "../models/Result.js"
import { logger } from "../utils/Logger.js"
import { api } from "./AxiosService.js"


class SearchService {

  async search(params) {
    logger.log('loading...')
    const res = await api.post('/search', params)
    logger.log('[RECEIVED DATA]', res.data)
    AppState.searchResults = res.data.map(i => new Result(i))
  }
}

export const searchService = new SearchService()