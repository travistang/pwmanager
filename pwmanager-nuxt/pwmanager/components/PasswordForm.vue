<template>
  <mu-dialog
    :open="open"
    :title="isEdit?'Edit Password':'AddPassword'"
    @close="onClose"
  >
    <!-- left half-->
    <mu-flexbox>
      <mu-flexbox-item>
        <mu-content-block>
          <mu-text-field
            hintText="Password Name"
            type="text"
            icon="contact_mail"
            :disabled="isEdit"
            :value="passwordName"
            :rowsMax="2"
            fullWidth
          />
          <br/>
          <mu-text-field
            hintText="Password"
            type="text"
            icon="vpn_key"
            :value="passwordOrNull"
            :rowsMax="2"
            disabled
            fullWidth
          />
          <br/>
          <mu-flat-button
            label="Generate Password"
            class="demo-flat-button"
            :disabled="!isValidCriteria"
            @click="generatePassword"
            primary/>
        </mu-content-block>
      </mu-flexbox-item>
    <!-- right half -->
      <mu-flexbox-item>
        <mu-content-block>

          Password of {{passwordName}} contains:
          <mu-paper>
              <mu-chip
                v-for="(contain,cat) in passwordContains"
                @click="toggle(cat);generatePassword"
                :backgroundColor="contain?'deepPurple400':'grey300'"
                :class="contain?'chip-selected':'chip'"

                >
                <mu-avatar :size="32">{{getAvatar(cat)}}</mu-avatar>
                {{catRepr(cat)}}
              </mu-chip>
          </mu-paper>
          <!-- <br/> -->
        </mu-content-block>
        <mu-content-block>
          Password Length: {{passwordLength}}
          <mu-slider v-model="passwordLength"
            :min="numCriteria || 1"
            :max="32"
            :step="1"
            :disabled="!isValidCriteria"
            @change="generatePassword"
          />
        </mu-content-block>
      </mu-flexbox-item>
    </mu-flexbox>
    <mu-flat-button
      slot="actions"
      @click="onClose"
      secondary
      label="Cancel"
    />
    <mu-flat-button
      slot="actions"
      primary
      @click="onAction"
      :label="isEdit?'Update Password':'Create Password'"
      :disabled="!isValidCriteria"
    />
  </mu-dialog>
</template>

<script>
export default {
  props: {
    'password': {
      type: Object,
      validator: function(pw)
      {
        if (pw == null) return true
        return pw.name
            && pw.createdAt
            && pw.updatedAt
            && pw.password
            && pw.objectId
      }
    },
    'isEdit':   Boolean,
    'open':     Boolean,
    'onClose':  Function,
    'onAction': Function,
  },
  data () {
    return {

      passwordContains: {
        number: true,
        lowercase: true,
        uppercase: true,
        symbols: true,
      },
      passwordLength: 8,
    }
  },
  computed: {
    isValidCriteria: function()
    {
      // check if all of the criteria has been disabled
      if (!(Object.keys(this.passwordContains)
          .map((k) => this.passwordContains[k])
          .reduce((p,q) => p || q))) return false
      return true
    },
    numCriteria: function()
    {
      // get the number of criteria toggled on
      return Object.keys(this.passwordContains)
          .map((k) => this.passwordContains[k])
          .reduce((c,q) => q?(c + 1):c,0)
    },
    passwordName: function()
    {
      return this.password?this.password.name:null
    },
    passwordOrNull: function()
    {
      return this.password?this.password.password:null
    }
  },
  methods: {
    generatePassword: function()
    {
      // prepare functions
      const punc = "!@#$%^&*(){}:\"<>?\\\'/.,?><';[]|".split('')
      const alpha = "qwertyuiopasdfghjklzxcvbnm"
      const lower = alpha.split('')
      const upper = alpha.toUpperCase().split('')
      const nums = "1234567890".split('')

      // gather criteria
      let charPool = []
      let newPw = ''

      // and a helper function
      const draw = (list) => list[~~(Math.random() * list.length)]
      // start populating
      if(this.passwordContains.number){
        newPw += draw(nums)
        charPool = charPool.concat(nums)
      }
      if(this.passwordContains.lowercase){
        newPw += draw(lower)
        charPool = charPool.concat(lower)
      }
      if(this.passwordContains.uppercase){
        newPw += draw(upper)
        charPool = charPool.concat(upper)
      }
      if(this.passwordContains.symbols){
        newPw += draw(punc)
        charPool = charPool.concat(punc)
      }
      // and draw amoung the charPool...
      const charsRemain = this.passwordLength - newPw.length
      for(var i = 0; i < charsRemain; i++)
      {
          newPw += draw(charPool)
      }

      this.password.password = newPw

    },
    toggle: function(cat)
    {
      this.passwordContains[cat] = !this.passwordContains[cat]
    },
    catRepr: function(cat)
    {
      switch(cat)
      {
        case "number": return "Digits"
        case "lowercase": return "Lowercase"
        case "uppercase": return "Uppercase"
        default:
          return "Punctuations"
      }
    },
    getAvatar: function(cat)
    {
      switch(cat)
      {
        case "number": return "0"
        case "lowercase": return "a"
        case "uppercase": return "A"
        default:
          return "#"
      }
    },
  }
}
</script>
<style scoped>
.chip {
  margin: 4px;
  width: 45%;
}
.chip-selected{
  color: white;
  background-color:primary;
  margin:4px;
  width: 45%;
}
</style>
