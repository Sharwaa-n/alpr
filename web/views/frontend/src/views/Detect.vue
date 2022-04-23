<template>
  <div>
    <h3>Upload!</h3>
      


      <div v-if='!beingDetected'>
        <div class="main-image mt-4 mb-4" v-if='detectedMainImage'>
            <img class="image-rounded" :title='detectedMainImage.number' :src='getFile(detectedMainImage.plate)' alt="">
        </div>
        <div class="thumnails d-flex flex-wrap">
          <div class="d-flex flex-column align-items-center p-1" v-for='(img, i) in resolvedFiles' :key='i'>
            <img class="thumb" :class="{lost: img.lost}"  :src="getFile(img.plate)" :title='img.number'>
            <span>{{img.number}}</span>
          </div>
        </div>


        <v-upload
          class="file-picker"
          ref="upload"
          @file-chosen="inputFile"
          :preview='preview'
        >

        Upload file 
        </v-upload>

      </div>
      <div v-else class="loading d-flex justify-content-center align-items-center">
        <v-loader />
      </div>
  </div>
</template>

<script>

import Upload from '../components/Upload'
import Loader from '../components/Loader'
export default {
  components: {
    'v-upload': Upload,
    'v-loader': Loader,
  },
  computed: {
    preview() {
      return this.getFile(this.detectedMainImage);
    }
  },
  data() {
    return {
      files: [],
      uploadUrl: 'http://localhost:5000/detect',
      resolvedFiles: [],
      detectedMainImage: null,
      beingDetected: false,
    }
  },
  methods: {
    getFile(img) {
      if(img){
        return `http://localhost:5000/preview/${img}`
      }
    },
    inputFile: function (file) {

      let formData = new FormData();
      this.beingDetected = true;
      formData.append('image', file)
      this.$api.post(this.uploadUrl, formData).then(a => a.data).then(response => {
          let files = response.files;
          this.resolvedFiles = Object.keys(files).filter( i => i != 'detection').map(i => files[i]);
          this.detectedMainImage = files['detection']
      }).catch(err => {
        console.log(err);
      }).finally(( ) => this.beingDetected = false )

    },
  }

}
</script>

<style>

.loading {
  height: 20rem;
}

.image-rounded {
  border-radius: 10px;;
}
.main-image img {
  width: 100%;
}

.file-picker:hover {
  background: #BDBDBD;
    color: #fff;
}
.file-picker {
  cursor: pointer;
  transition: all .3s ease-in-out;
      width: 100%;
    min-height: 10rem;
    justify-content: center;
    display: flex !important;
    align-items: center;
    background: #F5F5F5;
    border-radius: 10px;
    color: #9E9E9E;
}

.thumnails .thumb {
  width: 120px;
  border-radius: 10px;
}

.lost {
  border: 6px solid #E53935;
}
</style>