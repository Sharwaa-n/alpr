<template>
  <div @click="pickFile" class="preview mb-4" >
      <input ref='file' @input="letPeepsKnow" type="file" class="hidden">
      <button class="btn">Upload</button>
  </div>
</template>

<script>
export default {
  


  data() {
    return {
      image: null,
      height: '20rem'
    }
  },
  
  methods: {
    pickFile() {
      this.$refs.file.click()
    },
    letPeepsKnow() {
      this.$emit('file-chosen', this.$refs.file.files[0])
    }
  }
}
</script>

<style>
  .hidden {
    display: none !important;
  }
  
</style>