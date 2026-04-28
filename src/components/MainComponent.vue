<template>
  <div class="main">
    <div class="map-panel">
      <!-- 日本列島ここが中心の碑 @37.5289367,137.1853999 -->
      <map-component
        ref="map"
        class="map-area"
        @location-found="onLocationFound"
        :latitude="37.5289367"
        :longitude="137.1853999"
        :zoom="5"
      />
      <div class="button-area d-flex justify-content-between align-items-center flex-row">
        <div class="d-flex justify-content-start align-items-center flex-row">
          <button
            @click="onLocateButtonClick"
            class="btn btn-primary m-0 px-4 py-1 text-nowrap"
            :disabled="trackButtonChecked"
          >
            現在位置の取得
          </button>
          <button
            @click="onRecordButtonClick"
            class="btn btn-primary mx-3 my-0 px-4 py-1 text-nowrap"
            :disabled="trackButtonChecked || !locationFoundEvent"
          >
            記録
          </button>
        </div>
        <div class="d-flex justify-content-end align-items-center flex-row">
          <div class="mx-3 my-0 p-0 text-nowrap">
            <label class="hide-on-small-screen form-check-label text-nowrap" for="trackButton"> 自動追跡 </label>
          </div>
          <div class="form-check form-switch">
            <input
              v-model="trackButtonChecked"
              @change="onTrackLocateButtonChange"
              class="form-check-input custom-switch"
              type="checkbox"
              role="switch"
              id="trackButton"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="log-panel">
      <div class="log-data">
        <data-table :data="logs" :columns="columns" :options="options" @select="showLocation2" class="display">
          <template #column-0="props">
            <div class="datetime-column">
              {{ getTimeString(props.rowData.timestamp) }}
            </div>
          </template>
          <template #column-1="props">
            <div class="address-column">
              {{ props.rowData.address }}
            </div>
          </template>
        </data-table>
      </div>
      <div class="footer-area d-flex flex-column justify-content-start align-items-center">
        <div class="mx-0 mb-2">
          <a href="https://github.com/yamakox/location-logger-fastapi">本アプリ</a>はデモ用として運用しています。<br />
          記録した位置情報は予告無く削除される場合があります。
        </div>
        <div class="m-0 p-0">CID: {{ cid }}</div>
        <div class="m-0 p-0">Version: {{ version }}</div>
        <div class="mx-0 mt-2">
          <a href="https://y-app.cc/">&copy; 2026 y-app</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MapComponent from './MapComponent.vue'
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net'
import 'datatables.net-select'
import axios from 'axios'

// クライアントのデバッグ用フラグ
const debugClient = false

// 開発時はローカルAPIを使用し、本番ビルド時は環境変数を使用する
const serverUrl = import.meta.env.VITE_API_BASE_URL || ''

// DataTableの初期化
DataTable.use(DataTablesCore)
const columns = [
  { data: 'timestamp', title: '記録日時', type: 'date' },
  { data: 'address', title: '地名' },
]
const options = {
  paging: false,
  searching: false,
  select: 'single',
  order: { name: 'timestamp', dir: 'desc' },
}

// 位置情報の一覧(最大300件)
const logs = ref([])
const maxLogCount = 300

// map-componentへのref
const map = ref()

// 自動追跡用チェックボックスへのref
const trackButtonChecked = ref(false)

// location-foundイベント発生時のイベントオブジェクトへのref
const locationFoundEvent = ref(null)

// Cookieのcidの値
const cid = ref('-----')
const version = ref('-----')

// 最後に選択した履歴の日付の午前0時のtimestamp
let lastTimestamp0 = null

// 日時書式
const dateFormat = {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
}
const timeFormat = {
  hour: '2-digit',
  minute: '2-digit',
}

// timestampから日時文字列の取得
function getTimeString(timestamp) {
  let date = new Date(timestamp)
  return date.toLocaleDateString([], dateFormat) + ' ' + date.toLocaleTimeString([], timeFormat)
}

// timestampからその日の午前0時のtimestampの算出
function getTimestamp0(timestamp) {
  let ds = new Date(timestamp).toLocaleDateString()
  return Date.parse(ds)
}

// 位置情報の履歴を地図上に表示する
function setLatLngs(timestamp) {
  let timestamp0 = getTimestamp0(timestamp)
  let latlngs = []
  if (timestamp != null) {
    let timestamp24 = timestamp0 + 24 * 3600 * 1000
    logs.value
      .filter((x) => timestamp0 <= x.timestamp && x.timestamp < timestamp24)
      .forEach((x) => {
        latlngs.push([x.latitude, x.longitude])
      })
  } else {
    logs.value.forEach((record) => {
      latlngs.push([record.latitude, record.longitude])
    })
  }
  map.value.setLatLngs(latlngs)
  if (lastTimestamp0 != timestamp0) {
    map.value.fitLatLngs()
    lastTimestamp0 = timestamp0
  }
}

// map-componentのイベントハンドラ
function onLocationFound(event) {
  locationFoundEvent.value = event
  if (trackButtonChecked.value) {
    postLocation()
  }
}

// 位置情報の履歴のイベントハンドラ
function showLocation(record) {
  setLatLngs(record.timestamp)
  map.value.showLocation(record.latitude, record.longitude, record.timestamp, record.address, record.distance)
}

function showLocation2(e, dt, type, index) {
  showLocation(logs.value[index])
  dt.rows().deselect()
}

// ボタンのイベントハンドラ
function onLocateButtonClick(event) {
  map.value.locate()
}

function onTrackLocateButtonChange(event) {
  if (trackButtonChecked.value) {
    console.log('onTrackLocateButtonChange: true')
    map.value.locate(true)
  } else {
    console.log('onTrackLocateButtonChange: false')
    map.value.stopLocate()
  }
}

async function onRecordButtonClick(event) {
  await postLocation()
}

function pushLog(record) {
  logs.value.unshift(record)
  window.scrollTo({ top: 0, behavior: 'instant' })
  setLatLngs(record.timestamp)
}

async function postLocation() {
  let e = locationFoundEvent.value
  locationFoundEvent.value = null
  let record = {
    timestamp: e.timestamp,
    latitude: e.latlng.lat,
    longitude: e.latlng.lng,
    address: e.address,
    distance: e.distance,
  }

  // `withCredentials: true`を指定すると、Cookieのcidの値を取得できる
  try {
    // https://zenn.dev/motoishimotoi/articles/925d04192e66f9
    // API Router側では'/location`の下に`/`を付けているため、
    // 呼び出し側も`/`を付けないと、307 Temporary Redirectが発生する。
    await axios.post(`${serverUrl}/api/v1/location/`, record, { withCredentials: true })
    if (logs.value.length >= maxLogCount) {
      logs.value.length = maxLogCount - 1
    }
    pushLog(record)
  } catch (error) {
    locationFoundEvent.value = e
    console.log(error)
    record.address = `${record.address}: 送信失敗`
    pushLog(record)
  }
}

// appマウント時の処理
onMounted(async () => {
  console.log('MainComponent.onMounted')
  try {
    // バージョン情報とCIDの取得
    const promiseVersion = axios.get(`${serverUrl}/api/v1/misc/version`, {
      withCredentials: true,
    })
    // 307 Temporary Redirectが発生するため、`/`を付ける
    const promiseClient = axios.get(`${serverUrl}/api/v1/client/`, {
      withCredentials: true,
    })
    const [resVersion, resClient] = await Promise.all([promiseVersion, promiseClient])
    version.value = resVersion.data?.version ?? '-----'
    cid.value = resClient.data?.cid ?? '-----'

    // 位置情報の一覧の取得
    if (!debugClient) {
      // 307 Temporary Redirectが発生するため、`/`を付ける
      const resLocation = await axios.get(`${serverUrl}/api/v1/location/`, {
        withCredentials: true,
      })
      logs.value = resLocation.data
      setLatLngs(null)
      if (logs.value.length > 1) {
        map.value.fitLatLngs()
      }
    } else {
      // for debugging
      logs.value = [
        {
          timestamp: new Date().getTime(),
          latitude: 35.6811124,
          longitude: 139.764516,
          address: '東京駅',
        },
        {
          timestamp: new Date().getTime() + 60000,
          latitude: 36.5780486,
          longitude: 136.6455965,
          address: '金沢駅',
        },
      ]
      setLatLngs(null)
      if (logs.value.length > 1) {
        map.value.fitLatLngs()
      }
    }
  } catch (error) {
    console.log(error)
  }
})
</script>

<style scoped>
.main {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100svh;
  overflow: hidden;
}

@media (orientation: portrait) {
  .main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: stretch;
  }

  .map-panel {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 60%;
  }

  .log-panel {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 40%;
  }
}

@media (orientation: landscape) {
  .main {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: stretch;
  }

  .map-panel {
    margin: 0;
    padding: 0;
    width: 60%;
    height: 100%;
  }

  .log-panel {
    margin: 0;
    padding: 0;
    width: 40%;
    height: 100%;
  }
}

.map-panel {
  background: white;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;

  .map-area {
    margin: 0;
    padding: 0;
    width: 100%;
    height: calc(100% - 4rem);
  }

  .button-area {
    margin: 0;
    padding: 0.5rem 1rem;
    width: 100%;
    height: 4rem;
  }
}

.log-panel {
  background: white;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  overflow-y: auto;

  .log-data {
    margin: 0;
    padding: 0 1rem;
    width: 100%;
  }

  .footer-area {
    font-size: x-small;
    margin: 1rem;
  }
}

.datetime-column {
  font-family: ui-monospace;
  white-space: nowrap;
}

.address-column {
  white-space: nowrap;
}

.custom-switch {
  transform: scale(1.6);
}

@media (max-width: 440px) {
  .hide-on-small-screen {
    display: none;
  }
}
</style>
