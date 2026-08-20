package com.townkart.app

import android.os.Bundle
import android.content.Intent
import android.speech.RecognizerIntent
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val Ink = Color(0xFF13251D)
private val Green = Color(0xFF146B42)
private val Mint = Color(0xFFDFF7E8)
private val Sand = Color(0xFFF7F6F0)
private val Orange = Color(0xFFFFB648)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { TownKartApp() }
    }
}

@Composable
fun TownKartApp() {
    var tab by remember { mutableIntStateOf(0) }
    MaterialTheme(colorScheme = lightColorScheme(primary = Green, background = Sand, surface = Color.White)) {
        Scaffold(
            containerColor = Sand,
            bottomBar = { AppBottomBar(tab, onSelect = { tab = it }) }
        ) { padding ->
            Box(Modifier.padding(padding)) {
                AnimatedContent(tab, label = "screen") { page ->
                    when (page) {
                        0 -> HomeScreen(onOpenImpact = { tab = 1 })
                        1 -> ImpactScreen()
                        else -> ProfileScreen()
                    }
                }
            }
        }
    }
}

@Composable
private fun HomeScreen(onOpenImpact: () -> Unit) {
    var query by remember { mutableStateOf("") }
    var reply by remember { mutableStateOf("Hi Aanya! I can help you find local, lower-impact choices. What do you need today?") }
    var showFlowerOptions by remember { mutableStateOf(false) }
    var reservedShop by remember { mutableStateOf<String?>(null) }
    val suggestions = listOf(
        Item("Fresh vegetables", "Green Basket", "0.8 km", "🥬", "12 pts"),
        Item("Organic filter coffee", "Maya Cafe", "1.1 km", "☕", "8 pts"),
        Item("Cotton tote bag", "Namma Store", "1.5 km", "👜", "20 pts")
    )
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 16.dp)
    ) {
        item { Header() }
        item { LocalMap() }
        item {
            Column(Modifier.padding(horizontal = 20.dp, vertical = 18.dp)) {
                Text("Your local guide", fontWeight = FontWeight.Bold, fontSize = 21.sp, color = Ink)
                Spacer(Modifier.height(10.dp))
                ChatCard(reply, query, onQueryChange = { query = it }, onSend = {
                    if (query.isNotBlank()) {
                        reply = when {
                            query.contains("flower", true) -> "I found fresh flower options under ₹500 from local sellers. Choose one below and I will reserve it for pickup."
                            query.contains("food", true) || query.contains("lunch", true) -> "Try a millet bowl from Green Spoon — it is nearby and earns 18 Green Points."
                            query.contains("gift", true) -> "I found handmade gift options at Namma Store, 1.5 km away."
                            else -> "Based on your recent choices, I recommend nearby sustainable shops with fast pickup."
                        }
                        showFlowerOptions = query.contains("flower", true)
                        query = ""
                    }
                })
                if (showFlowerOptions) {
                    Spacer(Modifier.height(12.dp))
                    FlowerChoices(reservedShop = reservedShop, onReserve = { reservedShop = it })
                }
                Spacer(Modifier.height(22.dp))
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text("Picked for you", fontWeight = FontWeight.Bold, fontSize = 21.sp, color = Ink)
                        Text("Based on your recent activity", fontSize = 13.sp, color = Color(0xFF64726B))
                    }
                    Text("See all", color = Green, fontWeight = FontWeight.SemiBold, modifier = Modifier.clickable { })
                }
                Spacer(Modifier.height(12.dp))
                LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    items(suggestions) { SuggestionCard(it) }
                }
                Spacer(Modifier.height(18.dp))
                GreenPointsStrip(onClick = onOpenImpact)
            }
        }
    }
}

@Composable private fun Header() = Row(
    Modifier.fillMaxWidth().padding(20.dp), verticalAlignment = Alignment.CenterVertically
) {
    Column(Modifier.weight(1f)) {
        Text("Good morning, Aanya", color = Ink, fontWeight = FontWeight.Bold, fontSize = 22.sp)
        Text("Perambalur • near you", color = Color(0xFF6E7B75), fontSize = 14.sp)
    }
    Box(Modifier.size(42.dp).clip(CircleShape).background(Mint), contentAlignment = Alignment.Center) {
        Text("A", color = Green, fontWeight = FontWeight.Bold, fontSize = 18.sp)
    }
}

@Composable private fun LocalMap() = Box(
    Modifier.fillMaxWidth().height(230.dp).padding(horizontal = 20.dp).clip(RoundedCornerShape(26.dp)).background(Color(0xFFE1EEE5))
) {
    Canvas(Modifier.fillMaxSize()) {
        val road = Color.White
        drawLine(road, Offset(-30f, 45f), Offset(size.width + 40f, size.height - 35f), 22f, cap = StrokeCap.Round)
        drawLine(road, Offset(size.width * .2f, -20f), Offset(size.width * .52f, size.height + 20f), 17f, cap = StrokeCap.Round)
        drawLine(road, Offset(size.width * .76f, -20f), Offset(size.width * .67f, size.height + 20f), 14f, cap = StrokeCap.Round)
        repeat(7) { i ->
            drawRoundRect(
                color = Color(0xFFA8CCB0),
                topLeft = Offset(18f + i * 51f, 32f + (i % 2) * 83f),
                size = androidx.compose.ui.geometry.Size(28f, 36f),
                cornerRadius = CornerRadius(5f, 5f)
            )
        }
    }
    Surface(Modifier.align(Alignment.TopStart).padding(16.dp), color = Color.White.copy(.92f), shape = RoundedCornerShape(14.dp), shadowElevation = 2.dp) {
        Row(Modifier.padding(horizontal = 12.dp, vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.LocationOn, null, tint = Green, modifier = Modifier.size(16.dp)); Spacer(Modifier.width(4.dp)); Text("Your area", fontSize = 12.sp, fontWeight = FontWeight.Bold)
        }
    }
    Column(Modifier.align(Alignment.Center), horizontalAlignment = Alignment.CenterHorizontally) {
        Box(Modifier.size(45.dp).background(Green, CircleShape), contentAlignment = Alignment.Center) { Icon(Icons.Default.Storefront, null, tint = Color.White) }
        Surface(color = Ink, shape = RoundedCornerShape(12.dp)) { Text("TownKart nearby", color = Color.White, fontSize = 12.sp, modifier = Modifier.padding(8.dp)) }
    }
    Surface(Modifier.align(Alignment.BottomCenter).padding(14.dp), color = Color.White, shape = RoundedCornerShape(18.dp), shadowElevation = 3.dp) {
        Row(Modifier.padding(horizontal = 14.dp, vertical = 10.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.NearMe, null, tint = Green, modifier = Modifier.size(18.dp)); Spacer(Modifier.width(7.dp)); Text("Explore shops around you", fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
        }
    }
}

@Composable private fun ChatCard(reply: String, query: String, onQueryChange: (String) -> Unit, onSend: () -> Unit) = Card(colors = CardDefaults.cardColors(containerColor = Ink), shape = RoundedCornerShape(22.dp)) {
    val voiceInput = rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        val spokenText = result.data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)?.firstOrNull()
        if (!spokenText.isNullOrBlank()) onQueryChange(spokenText)
    }
    Column(Modifier.padding(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Box(Modifier.size(34.dp).background(Orange, CircleShape), contentAlignment = Alignment.Center) { Icon(Icons.Default.AutoAwesome, null, tint = Ink, modifier = Modifier.size(19.dp)) }
            Spacer(Modifier.width(9.dp)); Text("Kart Companion", color = Color.White, fontWeight = FontWeight.Bold)
            Spacer(Modifier.weight(1f)); Text("Online", color = Color(0xFF9CE3B6), fontSize = 12.sp)
        }
        Spacer(Modifier.height(12.dp)); Text(reply, color = Color.White, fontSize = 14.sp, lineHeight = 20.sp)
        Spacer(Modifier.height(13.dp))
        Row(Modifier.fillMaxWidth().clip(RoundedCornerShape(14.dp)).background(Color.White.copy(.13f)).padding(start = 12.dp), verticalAlignment = Alignment.CenterVertically) {
            TextField(query, onQueryChange, modifier = Modifier.weight(1f), placeholder = { Text("Ask for a recommendation", color = Color.LightGray, fontSize = 13.sp) }, colors = TextFieldDefaults.colors(unfocusedContainerColor = Color.Transparent, focusedContainerColor = Color.Transparent, unfocusedTextColor = Color.White, focusedTextColor = Color.White, unfocusedIndicatorColor = Color.Transparent, focusedIndicatorColor = Color.Transparent), singleLine = true)
            IconButton(onClick = {
                voiceInput.launch(Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    putExtra(RecognizerIntent.EXTRA_PROMPT, "Say what you need from TownKart")
                })
            }) { Icon(Icons.Default.Mic, "Speak your request", tint = Color.White) }
            IconButton(onClick = onSend) { Icon(Icons.Default.ArrowUpward, "Send", tint = Ink, modifier = Modifier.clip(CircleShape).background(Orange).padding(6.dp)) }
        }
    }
}

private data class FlowerOption(val title: String, val seller: String, val price: String, val greenScore: String, val stock: String, val accent: Color)

@Composable private fun FlowerChoices(reservedShop: String?, onReserve: (String) -> Unit) {
    val options = listOf(
        FlowerOption("Mixed rose bouquet", "Meena Flowers • 0.6 km", "₹420", "92 / 100", "8 bouquets left", Color(0xFFFFE3E3)),
        FlowerOption("Jasmine garland", "Sri Lakshmi Florist • 1.0 km", "₹280", "96 / 100", "12 in stock", Color(0xFFFFF5D6))
    )
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text("Local options under ₹500", color = Ink, fontWeight = FontWeight.Bold, fontSize = 16.sp)
        options.forEach { option ->
            Card(shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Row(Modifier.padding(13.dp), verticalAlignment = Alignment.CenterVertically) {
                    Box(Modifier.size(52.dp).clip(RoundedCornerShape(14.dp)).background(option.accent), contentAlignment = Alignment.Center) { Text("💐", fontSize = 27.sp) }
                    Spacer(Modifier.width(11.dp))
                    Column(Modifier.weight(1f)) {
                        Text(option.title, fontWeight = FontWeight.Bold, color = Ink, fontSize = 14.sp)
                        Text(option.seller, color = Color(0xFF68766F), fontSize = 11.sp)
                        Spacer(Modifier.height(3.dp))
                        Text("${option.greenScore} green score  •  ${option.stock}", color = Green, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                    }
                    Column(horizontalAlignment = Alignment.End) {
                        Text(option.price, color = Ink, fontWeight = FontWeight.Bold, fontSize = 17.sp)
                        if (reservedShop == option.seller) Text("Reserved ✓", color = Green, fontWeight = FontWeight.Bold, fontSize = 11.sp)
                        else Button(onClick = { onReserve(option.seller) }, contentPadding = PaddingValues(horizontal = 10.dp, vertical = 2.dp), shape = RoundedCornerShape(10.dp)) { Text("Reserve", fontSize = 11.sp) }
                    }
                }
            }
        }
        if (reservedShop != null) Text("Reserved at $reservedShop. Show this screen at pickup.", color = Green, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
    }
}

private data class Item(val name: String, val shop: String, val distance: String, val emoji: String, val points: String)
@Composable private fun SuggestionCard(item: Item) = Card(Modifier.width(172.dp), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
    Column(Modifier.padding(13.dp)) {
        Box(Modifier.fillMaxWidth().height(76.dp).clip(RoundedCornerShape(13.dp)).background(Mint), contentAlignment = Alignment.Center) { Text(item.emoji, fontSize = 38.sp) }
        Spacer(Modifier.height(10.dp)); Text(item.name, fontWeight = FontWeight.Bold, color = Ink, maxLines = 1, overflow = TextOverflow.Ellipsis)
        Text(item.shop, fontSize = 12.sp, color = Color(0xFF6D7873)); Spacer(Modifier.height(7.dp))
        Row { Text(item.distance, fontSize = 12.sp, color = Green); Spacer(Modifier.weight(1f)); Text("+${item.points}", fontSize = 11.sp, color = Green, fontWeight = FontWeight.Bold) }
    }
}

@Composable private fun GreenPointsStrip(onClick: () -> Unit) = Card(Modifier.fillMaxWidth().clickable { onClick() }, colors = CardDefaults.cardColors(containerColor = Mint), shape = RoundedCornerShape(20.dp)) {
    Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
        Box(Modifier.size(42.dp).background(Green, CircleShape), contentAlignment = Alignment.Center) { Icon(Icons.Default.Eco, null, tint = Color.White) }
        Spacer(Modifier.width(12.dp)); Column(Modifier.weight(1f)) { Text("Green Points", fontWeight = FontWeight.Bold, color = Ink); Text("You earned 36 points this week", fontSize = 13.sp, color = Color(0xFF486156)) }
        Icon(Icons.Default.ChevronRight, null, tint = Green)
    }
}

@Composable private fun ImpactScreen() = LazyColumn(Modifier.fillMaxSize().padding(20.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
    item { Text("Your impact", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Ink); Text("Small choices, meaningful change.", color = Color(0xFF64726B)) }
    item { Card(colors = CardDefaults.cardColors(containerColor = Green), shape = RoundedCornerShape(26.dp)) { Column(Modifier.padding(22.dp)) { Text("GREEN POINTS", color = Color(0xFFC5F4D6), fontSize = 12.sp, letterSpacing = 1.sp); Text("1,240", color = Color.White, fontSize = 48.sp, fontWeight = FontWeight.Bold); Text("Level 3 • Local Champion", color = Color.White); Spacer(Modifier.height(12.dp)); LinearProgressIndicator(.68f, Modifier.fillMaxWidth().height(8.dp).clip(CircleShape), color = Orange, trackColor = Color.White.copy(.25f)); Spacer(Modifier.height(7.dp)); Text("260 points to the next reward", color = Color.White, fontSize = 12.sp) } } }
    item { Text("This month", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Ink) }
    item { Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) { Metric("12", "local orders", "🏪", Modifier.weight(1f)); Metric("4.2 kg", "CO₂ saved", "☁️", Modifier.weight(1f)); Metric("₹180", "local rewards", "✨", Modifier.weight(1f)) } }
    item { Card(shape = RoundedCornerShape(20.dp)) { Column(Modifier.padding(18.dp)) { Text("Your next reward", fontWeight = FontWeight.Bold, color = Ink); Spacer(Modifier.height(8.dp)); Text("Get ₹50 off at a local business when you reach 1,500 points.", color = Color(0xFF61716A), fontSize = 14.sp) } } }
}
@Composable private fun Metric(value: String, caption: String, emoji: String, modifier: Modifier) = Card(modifier, colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(18.dp)) { Column(Modifier.padding(12.dp)) { Text(emoji, fontSize = 20.sp); Text(value, fontWeight = FontWeight.Bold, color = Ink, fontSize = 17.sp); Text(caption, fontSize = 11.sp, color = Color(0xFF6D7873)) } }

@Composable private fun ProfileScreen() = LazyColumn(Modifier.fillMaxSize().padding(20.dp), verticalArrangement = Arrangement.spacedBy(15.dp)) {
    item { Text("Profile", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Ink) }
    item { Row(verticalAlignment = Alignment.CenterVertically) { Box(Modifier.size(74.dp).background(Mint, CircleShape), contentAlignment = Alignment.Center) { Text("A", color = Green, fontWeight = FontWeight.Bold, fontSize = 30.sp) }; Spacer(Modifier.width(16.dp)); Column { Text("Aanya Raman", fontWeight = FontWeight.Bold, fontSize = 21.sp, color = Ink); Text("aanya@email.com", color = Color(0xFF67756E)); Text("TownKart member since 2026", fontSize = 12.sp, color = Green) } } }
    item { Text("Account", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Ink) }
    items(listOf("Your orders" to Icons.Default.ReceiptLong, "Saved places" to Icons.Default.Bookmark, "Notifications" to Icons.Default.Notifications, "Help & support" to Icons.Default.HelpOutline)) { (title, icon) -> Card(shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) { Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) { Icon(icon, null, tint = Green); Spacer(Modifier.width(13.dp)); Text(title, Modifier.weight(1f), fontWeight = FontWeight.Medium, color = Ink); Icon(Icons.Default.ChevronRight, null, tint = Color.Gray) } } }
}

@Composable private fun AppBottomBar(current: Int, onSelect: (Int) -> Unit) = NavigationBar(containerColor = Color.White) {
    listOf("Home" to Icons.Default.Home, "Impact" to Icons.Default.Eco, "Profile" to Icons.Default.Person).forEachIndexed { index, (label, icon) ->
        NavigationBarItem(selected = current == index, onClick = { onSelect(index) }, icon = { Icon(icon, label) }, label = { Text(label) }, colors = NavigationBarItemDefaults.colors(selectedIconColor = Green, selectedTextColor = Green, indicatorColor = Mint))
    }
}
