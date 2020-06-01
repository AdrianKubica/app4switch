<template>
  <div class="hello">
    <b-card>
      <b-row>
        <b-col cols="6" offset="3" class="my-4">
          <b-input-group class="mt-3">
              <b-form-file
              name="file"
              v-model="file"
              :state="Boolean(file)"
              placeholder="Choose a file or drop it here..."
              drop-placeholder="Drop file here..."
              class="switch-input-file"
              ></b-form-file>
            <b-button :disabled="loading" @click="getSwitchData" variant="outline-success">Send</b-button>
          </b-input-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="10" offset="1" class="my-4">
          <b-table
          :items="results"
          :fields="fields"
          v-if="!loading"
          :striped="true"
          ></b-table>
          <b-spinner v-else variant="primary"></b-spinner>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { SwitchAPI } from "@/api/switch";


@Component
export default class HelloWorld extends Vue {

  private file: any = [];
  private results = [];
  private loading = false;

  private fields = [
    {
      key: 'key',
      sortable: true
    },
    {
      key: 'nr_week',
      sortable: true
    },{
      key:'day',
      sortable: true
    }, {
      key: 'observation_counter',
      sortable: true
    },
    {
      key: 'avg_day',
      sortable: true
    },
    {
      key: 'avg_week',
      sortable: true
    }
  ];

  async getSwitchData() {
    this.loading = true;
    const formData = new FormData();
    formData.append('file', this.file);
    try {
      const res = await SwitchAPI.getSwitchData(formData);
      this.results = res?.result;
      this.loading = false
      this.$bvToast.toast(`Successfully read switch data from server`, {
        title: 'App4Switch',
        autoHideDelay: 5000,
        variant: 'success'
      })
    } catch(err) {
        this.$bvToast.toast(`Some error occured: ${err.message}`, {
          title: 'App4Switch',
          autoHideDelay: 5000,
          variant: 'danger'
        })
    }
  }
}
</script>

<style scoped lang="scss">
  button:disabled {
   background-color: #E9ECEF;
  }

  .switch-input-file {
    cursor: pointer;
  }
</style>
